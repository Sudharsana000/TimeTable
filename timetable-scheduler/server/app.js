const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/generate', (req, res) => {
    const python = spawn('python', ['../python/genetic_algorithm.py']);

    let dataChunks = [];

    python.stdout.on('data', (data) => {
        dataChunks.push(data);
    });

    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        if (code === 0) {
            const output = Buffer.concat(dataChunks).toString();
            try {
                const timetables = JSON.parse(output);
                if (timetables.class1 && timetables.class2) {
                    res.json({
                        class1: timetables.class1,
                        class2: timetables.class2
                    });
                } else {
                    res.status(500).send('Incomplete timetables received from Python script');
                }
            } catch (error) {
                console.error(`Error processing JSON: ${error}`);
                res.status(500).send('Error parsing timetables');
            }
        } else {
            res.status(500).send('Python script failed to execute');
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});
