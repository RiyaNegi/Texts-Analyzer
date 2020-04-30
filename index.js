// express setup
const express = require('express')
const app = express()
const port = 5000
// parse request body
app.use(express.urlencoded())

app.use(express.static('public'));

// hbs setup
var exphbs  = require('express-handlebars');
app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');

// MySQL Setup
var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'password',
  database : 'analyzer'
});

connection.connect();
util = require('util')
connection.query = util.promisify(connection.query);

// moment
const moment = require('moment')

app.get('/', function (req, res) {
  res.render('home');
})

app.get('/mostchatted', async function (req, res) {
  chatCounts = await connection.query(`SELECT users.name, chat_counts.count FROM chat_counts INNER JOIN users ON users.id=chat_counts.user_id;`)
  labels = []
  data = []
  chatCounts.forEach((element) => {
    labels.push(element.name)
    data.push(element.count)
  });
  res.render('mostchatted', { labels: labels, data: data })
})

app.get('/sentiments', async function (req, res) {
  sentiments = await connection.query(`SELECT users.name, sentiments.* FROM sentiments INNER JOIN users ON users.id=sentiments.user_id;`)
  sentiment_data = null
  if(req.param('userId')) {
    sentiment_data = sentiments.find((element) => {
      return element.user_id === parseInt(req.param('userId'))
    });
  }
  res.render('sentiments', { sentiments: sentiments, sentiment_data: sentiment_data })
})

app.get('/chat_frequencies', async function (req, res) {
  frequencies = await connection.query(`SELECT users.name, chat_frequencies.* FROM chat_frequencies INNER JOIN users ON users.id=chat_frequencies.user_id;`)
  freq_data = null
  if(req.param('userId')) {
    freq_data = frequencies.find((element) => {
      return element.user_id === parseInt(req.param('userId'))
    });
    freq_data.data = freq_data.frequency.split(',').map((freq) => {
      return freq.match(/(?<=: )[0-9]+/)[0];
    });
  }

  res.render('chat_frequencies', { frequencies: frequencies, freq_data: freq_data })
})



app.listen(port)

console.log("App started!")
