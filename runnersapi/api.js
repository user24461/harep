const express = require('express');
const router = express.Router();
const sqlite3 = require('sqlite3')

const database = '../config/runners/runners.db'

router.get('/', (req, res) => {
  res.send('api ready');
});


/* /meetwaarde?year=YYYY */
router.get('/meetwaarde', (req, res) => {
  var year = parseInt(req.query.year);
  var year0 = (year + 0).toString() + "-01-01";
  var year1 = (year + 1).toString() + "-01-01";
  var db = new sqlite3.Database(database);
  var rows = db.all('select date, julianday(?) - julianday(?) as days, julianday(date) - julianday(?) as day,  minutes from meetwaarde where cast(substr(date, 1, 4) as integer) = ?', 
    [year1, year0, year0, year],
    (err, rows) => {
    res.send(rows);  
  }); 
  db.close();
});


/* /totaal?year=YYYY */
router.get('/totaal', (req, res) => {
  var year  = parseInt(req.query.year);
  var db = new sqlite3.Database(database);
  var rows = db.all('select cast(substr(date, 6, 2) as integer) as maand, sum(minutes) as minutes from meetwaarde where cast(substr(date, 1, 4) as integer) = ? group by cast(substr(date, 6, 2) as integer)', 
    [year],
    (err, rows) => {
      res.send(rows);  
  }); 
  db.close();
});


/* POST /meetwaarde   body => date=YYYY-MM-DD&miutes=XX */
router.post('/meetwaarde', (req, res) => {
  var date    = req.body.date;
  var minutes = parseInt(req.body.minutes); 
  var db = new sqlite3.Database(database);
  db.run('insert into meetwaarde (date, minutes) values(?,?)', [date, minutes]); 
  db.close();
  res.end();
});


/* DELETE /meetwaarde  body => date=YYYY-MM-DD */
router.delete('/meetwaarde', (req, res) => {
  console.log(req.body);
  var date    = req.body.date;
  var db = new sqlite3.Database(database);
  db.run('delete from meetwaarde where date = ?', [date]); 
  db.close();
  res.end();
});


module.exports = router;

