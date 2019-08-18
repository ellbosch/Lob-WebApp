// const bodyParser = require('body-parser');
const express = require('express');
const path = require('path');

const app = express();
const API_PORT = process.env.HTTP_PORT || 3001;

app.use(express.static(path.join(__dirname, '../client/build')));
// app.use(bodyParser.json());

app.get('/', function(req, res) {
	res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});

// create router for bloomfilter
// var bfRouter = express.Router();

// // gets info on bloom filter (i.e. it's size)
// bfRouter.get('/', function(req, res) {
// 	res.json(
// 		{
// 			size: bf.sizePowerOfTen,
// 			algorithms: { 'MD5': this.usesMd5, 'SHA-1': this.usesSha1, 'SHA-256': this.usesSha256 }
// 		});
// });

// // creates new bloom filter and sets size of bit vector
// bfRouter.post('/', function(req, res, next) {
// 	var sizePowerOfTen = req.body.size;
// 	var algorithms = req.body.algorithms;

// 	try {
// 		bf = new bloomfilter(sizePowerOfTen=sizePowerOfTen, usesMd5=algorithms['MD5'],
// 				usesSha1=algorithms['SHA-1'], usesSha256=algorithms['SHA-256']);
// 		bf.createStore();
// 		res.json(
// 			{
// 				size: bf.sizePowerOfTen,
// 				algorithms: { 'MD5': bf.usesMd5, 'SHA-1': bf.usesSha1, 'SHA-256': bf.usesSha256 }
// 			});
// 	} catch(err) {
// 		next(err.toString());
// 	}
// });

// // search word in bloomfilter
// bfRouter.get('/:word', function(req, res) {
// 	const result = bf.contains(req.params.word);
// 	res.json({ contains: result });
// });

// app.use('/bloomfilter', bfRouter);

// // catch errors at very end
// app.use(function (err, req, res, next) {
// 	res.status(500).json({ error: err });
// });

// launch our backend into a port
app.listen(API_PORT, () => console.log(`LISTENING ON PORT ${API_PORT}`));