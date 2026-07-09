const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.json());

// ── Load JSON data files (works locally and in Docker) ──────────────────────
const reviews_data = JSON.parse(
  fs.existsSync("reviews.json")
    ? fs.readFileSync("reviews.json", 'utf8')
    : fs.readFileSync("data/reviews.json", 'utf8')
);
const dealerships_data = JSON.parse(
  fs.existsSync("dealerships.json")
    ? fs.readFileSync("dealerships.json", 'utf8')
    : fs.readFileSync("data/dealerships.json", 'utf8')
);

// ── In-memory store (used when MongoDB is unavailable) ───────────────────────
let reviews_store = [...reviews_data['reviews']];
let dealerships_store = [...dealerships_data['dealerships']];

// ── Optionally connect to MongoDB ─────────────────────────────────────────────
let mongoConnected = false;
let Reviews, Dealerships;

try {
  const mongoose = require('mongoose');
  const mongoURL = process.env.MONGO_URL || "mongodb://localhost:27017/";

  mongoose.connect(mongoURL, { dbName: 'dealershipsDB', serverSelectionTimeoutMS: 3000 })
    .then(async () => {
      console.log('MongoDB connected ✓');
      mongoConnected = true;
      Reviews = require('./review');
      Dealerships = require('./dealership');
      // Seed data
      await Reviews.deleteMany({});
      await Reviews.insertMany(reviews_store);
      await Dealerships.deleteMany({});
      await Dealerships.insertMany(dealerships_store);
      console.log('Database seeded ✓');
    })
    .catch(err => {
      console.warn('MongoDB unavailable, using in-memory JSON store:', err.message);
    });
} catch (err) {
  console.warn('Mongoose not available, running in JSON-only mode:', err.message);
}

// ── Helper: fetch from Mongo or in-memory ────────────────────────────────────
async function getReviews(filter = {}) {
  if (mongoConnected && Reviews) return Reviews.find(filter);
  let data = reviews_store;
  if (filter.dealership !== undefined)
    data = data.filter(r => String(r.dealership) === String(filter.dealership));
  return data;
}

async function getDealerships(filter = {}) {
  if (mongoConnected && Dealerships) return Dealerships.find(filter);
  let data = dealerships_store;
  if (filter.state) data = data.filter(d => d.state === filter.state);
  return data;
}

// ── Routes ────────────────────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    res.json(await getReviews());
  } catch (e) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Fetch reviews by dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    res.json(await getReviews({ dealership: req.params.id }));
  } catch (e) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    res.json(await getDealerships());
  } catch (e) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    if (state === 'All') return res.json(await getDealerships());
    res.json(await getDealerships({ state }));
  } catch (e) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Fetch a single dealer by id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    let dealers;
    if (mongoConnected && Dealerships) {
      dealers = await Dealerships.find({ id: req.params.id });
    } else {
      dealers = dealerships_store.filter(d => String(d.id) === String(req.params.id));
    }
    if (dealers.length > 0) res.json(dealers[0]);
    else res.status(404).json({ error: 'Dealer not found' });
  } catch (e) {
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Insert a review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = JSON.parse(req.body);
    const maxId = reviews_store.reduce((m, r) => Math.max(m, r.id || 0), 0);
    const newReview = {
      id: maxId + 1,
      name: data['name'],
      dealership: data['dealership'],
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    };

    if (mongoConnected && Reviews) {
      const saved = await new Reviews(newReview).save();
      res.json(saved);
    } else {
      reviews_store.push(newReview);
      res.json(newReview);
    }
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
