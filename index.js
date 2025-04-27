const express = require("express");
const bodyParser = require("body-parser");
const { google } = require("googleapis");
const fs = require("fs");
const stream = require("stream");
const bcrypt = require("bcryptjs");
require("dotenv").config();

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// Load and parse the service account credentials
let serviceAccount;
try {
  serviceAccount = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT);
} catch (err) {
  console.error("❌ Failed to load service account JSON:", err.message);
  process.exit(1);
}

// try {
//   serviceAccount = JSON.parse(
//     fs.readFileSync("./service_account.json", "utf8"),
//   );
//   console.log(serviceAccount);
// } catch (err) {
//   console.error("❌ Failed to load service account JSON:", err.message);
//   process.exit(1);
// }

// Set up Google Drive authentication
const auth = new google.auth.GoogleAuth({
  credentials: serviceAccount,
  scopes: ["https://www.googleapis.com/auth/drive"],
});

const drive = google.drive({ version: "v3", auth });

const sheets = google.sheets({ version: "v4", auth });

const SPREADSHEET_ID = process.env.SPREADSHEET_ID;

// Test endpoint
app.get("/test", async (req, res) => {
  res.status(200).json({ response: "Hello world" });
});

async function ensureSheetHeader(sheet, SPREADSHEET_ID) {
  const header = [
    "Time",
    "Grow Light Status",
    "Water Level",
    "Humidity",
    "pH Level",
  ];

  // Check if the sheet has data
  const existing = await sheets.spreadsheets.values.get({
    spreadsheetId: SPREADSHEET_ID,
    range: `${sheet}!A1:E1`,
  });

  if (!existing.data.values || existing.data.values.length === 0) {
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: `${sheet}!A1:E1`,
      valueInputOption: "USER_ENTERED",
      resource: { values: [header] },
    });
  }
}

async function ensureSheetExists(sheetName) {
  const spreadsheet = await sheets.spreadsheets.get({
    spreadsheetId: SPREADSHEET_ID,
  });

  const sheetExists = spreadsheet.data.sheets.some(
    (s) => s.properties.title === sheetName,
  );

  if (!sheetExists) {
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId: SPREADSHEET_ID,
      resource: {
        requests: [
          {
            addSheet: {
              properties: {
                title: sheetName,
              },
            },
          },
        ],
      },
    });
  }
}

app.post("/data", async (req, res) => {
  const {
    arduinoTime,
    growLightsStatus,
    waterLevelDistance,
    humidity,
    pHLevel,
  } = req.body;
  // const SPREADSHEET_ID = "17Q0-wDURshAZycye4zLDHclQ0VFzQwl-SDlCMeGaIdk";
  const sheet = "hydroponics";
  const values = [
    [
      new Date(arduinoTime).toLocaleString(),
      growLightsStatus,
      waterLevelDistance,
      humidity,
      pHLevel,
    ],
  ];

  // if (!readTimestamp || !value || !sensor) {
  //   return res.status(400).json({ error: "Important data not provided" });
  // }

  try {
    await ensureSheetExists(sheet);
    await ensureSheetHeader(sheet, SPREADSHEET_ID);

    await sheets.spreadsheets.values.append({
      spreadsheetId: SPREADSHEET_ID,
      range: `${sheet}!A:E`,
      valueInputOption: "USER_ENTERED",
      resource: { values },
    });

    // await formatSheet(sheet, values); // Optional
    res.status(200).json({ message: "Data saved" });
  } catch (err) {
    console.error("❌ Error saving data:", err);
    res.status(500).json({ error: "Failed to save data." });
  }
});

app.post("/user", async (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ error: "Important data not provided" });
  }

  try {
    const hashedPassword = await bcrypt.hash(password, 10); // 10 = salt rounds
    const values = [[new Date().toLocaleString(), username, hashedPassword]];

    await ensureSheetExists(sheet);

    await sheets.spreadsheets.values.append({
      spreadsheetId: SPREADSHEET_ID,
      range: `${sheet}!A:C`,
      valueInputOption: "USER_ENTERED",
      resource: { values },
    });

    // await formatSheet(sheet, values); // Optional
    res.status(200).json({ message: "Data saved" });
  } catch (err) {
    console.error("❌ Error saving data:", err);
    res.status(500).json({ error: "Failed to save data." });
  }
});

app.get("/data/:sheet", async (req, res) => {
  const sheet = req.params.sheet;

  try {
    const result = await sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET_ID,
      range: `${sheet}!A:E`, // Adjust columns as needed
    });

    const rows = result.data.values;
    if (!rows || rows.length === 0) {
      return res.status(404).json({ message: "No data found." });
    }

    // Optionally return the data as an array of objects with headers
    const [headers, ...data] = rows;
    const formattedData = data.map((row) =>
      headers.reduce((obj, header, i) => {
        obj[header] = row[i] || "";
        return obj;
      }, {}),
    );

    res.status(200).json(formattedData);
  } catch (err) {
    console.error("❌ Error reading data:", err);
    res.status(500).json({ error: "Failed to read data." });
  }
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

app.get("/data/:sheet", async (req, res) => {
  const sheet = req.params.sheet;

  try {
    const result = await sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET_ID,
      range: `${sheet}!A:E`, // Adjust columns as needed
    });

    const rows = result.data.values;
    if (!rows || rows.length === 0) {
      return res.status(404).json({ message: "No data found." });
    }

    // Optionally return the data as an array of objects with headers
    const [headers, ...data] = rows;
    const formattedData = data.map((row) =>
      headers.reduce((obj, header, i) => {
        obj[header] = row[i] || "";
        return obj;
      }, {}),
    );

    res.status(200).json(formattedData);
  } catch (err) {
    console.error("❌ Error reading data:", err);
    res.status(500).json({ error: "Failed to read data." });
  }
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
