const express = require("express");
const bodyParser = require("body-parser");
const { google } = require("googleapis");
const fs = require("fs");
const stream = require("stream");
require("dotenv").config();

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// Load and parse the service account credentials
let serviceAccount;
// try {
//   const serviceAccount = JSON.parse(
//     Buffer.from(process.env.GOOGLE_SERVICE_ACCOUNT, "base64").toString("utf8"),
//   );
// } catch (err) {
//   console.error("❌ Failed to load service account JSON:", err.message);
//   process.exit(1);
// }

try {
  serviceAccount = JSON.parse(
    fs.readFileSync("./service_account.json", "utf8"),
  );
} catch (err) {
  console.error("❌ Failed to load service account JSON:", err.message);
  process.exit(1);
}

// Set up Google Drive authentication
const auth = new google.auth.GoogleAuth({
  credentials: serviceAccount,
  scopes: ["https://www.googleapis.com/auth/drive"],
});

const drive = google.drive({ version: "v3", auth });

// Test endpoint
app.get("/test", async (req, res) => {
  res.status(200).json({ response: "Hello world" });
});

// POST endpoint to upload an image to Google Drive
app.post("/upload-image", async (req, res) => {
  try {
    const { filename, mimeType, imageBase64 } = req.body;
    if (!filename || !mimeType || !imageBase64) {
      return res
        .status(400)
        .json({ error: "Missing filename, mimeType or imageBase64" });
    }

    // Convert base64 string to a buffer
    const buffer = Buffer.from(imageBase64, "base64");
    console.log(buffer);
    // Create a stream from the buffer
    const bufferStream = new stream.PassThrough();
    bufferStream.end(buffer);

    const fileMetadata = {
      name: filename,
      parents: [process.env.FOLDER_ID], // Replace with actual folder ID
    };
    const media = {
      mimeType,
      body: bufferStream,
    };

    const response = await drive.files.create({
      resource: fileMetadata,
      media: media,
      fields: "id",
    });

    res.status(200).json({ fileId: response.data.id });
  } catch (err) {
    console.error("Error uploading image:", err);
    res.status(500).json({ error: err.message });
  }
});

// GET endpoint to retrieve an image from Google Drive by fileId
app.get("/images/:folderId", async (req, res) => {
  try {
    const folderId = req.params.folderId;

    // Query to get images in the folder
    const query = `'${folderId}' in parents and mimeType contains 'image/' and trashed = false`;

    const response = await drive.files.list({
      q: query,
      fields: "files(id, name)",
    });

    const files = response.data.files || [];

    // Generate direct download links
    const links = files.map((file) => ({
      id: file.id,
      name: file.name,
      downloadUrl: `https://drive.google.com/uc?export=download&id=${file.id}`,
    }));

    res.status(200).json({ images: links });
  } catch (err) {
    console.error("Error retrieving image links:", err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
