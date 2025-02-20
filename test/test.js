import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs';
import path from 'path';
import FormData from 'form-data';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function uploadImage() {
    const fetch = (await import('node-fetch')).default;

    const form = new FormData();
    const imagePath = path.join(__dirname, 'test1.jpg'); // Replace with your image path

    form.append('image', fs.createReadStream(imagePath));

    try {
        const response = await fetch('http://localhost:7860/', {
            method: 'POST',
            body: form
        });

        const data = await response.json();
        console.log('Success:', data);
    } catch (error) {
        console.error('Error:', error);
    }
}

uploadImage();
