const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));

mongoose.connect("mongodb://localhost:27017/",{'dbName':'dealershipsDB'})
  .then(() => {
    console.log('Connected to MongoDB');
    const Reviews = require('./review');
    const Dealerships = require('./dealership');

    // Populate data
    Reviews.deleteMany({}).then(()=>{
      Reviews.insertMany(reviews_data['reviews']);
      console.log('Reviews inserted');
    }).catch(err => console.error('Error inserting reviews:', err));
    
    Dealerships.deleteMany({}).then(()=>{
      Dealerships.insertMany(dealerships_data['dealerships']);
      console.log('Dealerships inserted');
    }).catch(err => console.error('Error inserting dealerships:', err));
  })
  .catch(err => {
    console.error('MongoDB connection error:', err);
    console.log('Server will start but database operations will fail');
  });

const Reviews = require('./review');
const Dealerships = require('./dealership');


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    if (documents.length === 0) {
      // If no documents found in DB, try mock data
      const mockReviews = reviews_data['reviews'].filter(r => r.dealership == req.params.id);
      return res.json(mockReviews);
    }
    res.json(documents);
  } catch (error) {
    console.error('Error fetching reviews:', error.message);
    // Return mock data if MongoDB is not connected
    const mockReviews = reviews_data['reviews'].filter(r => r.dealership == req.params.id);
    if (mockReviews.length > 0) {
      return res.json(mockReviews);
    }
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    if (documents.length === 0) {
      // If no documents found in DB, try mock data
      return res.json(dealerships_data['dealerships']);
    }
    res.json(documents);
  } catch (error) {
    console.error('Error fetching dealerships:', error.message);
    // Return mock data if MongoDB is not connected
    return res.json(dealerships_data['dealerships']);
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({state: req.params.state});
    if (documents.length === 0) {
      // If no documents found in DB, try mock data
      const mockDealers = dealerships_data['dealerships'].filter(d => d.state === req.params.state);
      return res.json(mockDealers);
    }
    res.json(documents);
  } catch (error) {
    console.error('Error fetching dealerships by state:', error.message);
    // Return mock data if MongoDB is not connected
    const mockDealers = dealerships_data['dealerships'].filter(d => d.state === req.params.state);
    if (mockDealers.length > 0) {
      return res.json(mockDealers);
    }
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const documents = await Dealerships.find({id: req.params.id});
    if (documents.length === 0) {
      // If no documents found in DB, try mock data
      const mockDealer = dealerships_data['dealerships'].filter(d => d.id == req.params.id);
      return res.json(mockDealer);
    }
    res.json(documents);
  } catch (error) {
    console.error('Error fetching dealer:', error.message);
    // Return mock data if MongoDB is not connected
    const mockDealer = dealerships_data['dealerships'].filter(d => d.id == req.params.id);
    if (mockDealer.length > 0) {
      return res.json(mockDealer);
    }
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents[0]['id']+1

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
