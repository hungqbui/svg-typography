import express from 'express';
import sharp from 'sharp';
import multer from 'multer';

const app = express();

const storage = multer.memoryStorage();
const upload = multer({ storage });

const convertSvgToPng = async (svgBuffer) => {

    const buffer = await sharp(svgBuffer).png().toBuffer();
    const base64 = buffer.toString('base64');

    return base64;
}


app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.post('/convert', upload.single("file"), (req, res) => {
    
    console.log(req.file.buffer.length);

    convertSvgToPng(req.file.buffer).then((base64) => {
        console.log(base64)
        res.send(base64);
    })

});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});