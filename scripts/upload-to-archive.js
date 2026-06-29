#!/usr/bin/env node
/**
 * upload-to-archive.js
 *
 * Uploads a final video to the Vocal Image Google Drive Archive.
 * Creates the YYYY.MM folder if it doesn't exist yet.
 *
 * Usage:
 *   node scripts/upload-to-archive.js <video_path> [title]
 *   node scripts/upload-to-archive.js output/S268_V1.mov
 *   node scripts/upload-to-archive.js output/S268_V1.mov "S268_V1"
 *
 * Requires: GOOGLE_SERVICE_ACCOUNT_KEY env var (path to service account JSON)
 * OR: run via Claude Code which has Drive MCP access
 */

import { readFileSync, existsSync } from 'fs';
import { basename, extname } from 'path';
import { google } from 'googleapis';

const ARCHIVE_FOLDER_ID = process.env.GOOGLE_DRIVE_ARCHIVE_ID || '1zeTJs-UpzHp_a6myXAFHs8G2CP5zPpos';

// Known monthly folder IDs (update as new months are created)
const MONTHLY_FOLDERS = {
  '2026.07': '14hXRT693Lj9J_OMrT3eLOD3NRQooElcL',
  '2026.06': '1R41eCe9wdFwve3NfGU4kPnCSKM_57yBl',
  '2026.05': '19xFpK9ZnYTjwq7mOxdyEiNC6FeGQWQwP',
  '2026.04': '1xBrR8mIjylwZFtNBcC_nC5TO3KzfWU0I',
  '2026.03': '186VPAfn3J0aMu9JN1eNCkqPKdf3Vp3gi',
  '2026.02': '1ZsfEZ5-Cj03Tu3wKjyNlwoITPlpmKkXp',
  '2026.01': '1VhJKFsEmwLQqxbj_0SpvQcnCx_feDktL',
};

function getCurrentMonthKey() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  return `${year}.${month}`;
}

function getMimeType(filePath) {
  const ext = extname(filePath).toLowerCase();
  const map = {
    '.mp4': 'video/mp4',
    '.mov': 'video/quicktime',
    '.webm': 'video/webm',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
  };
  return map[ext] || 'application/octet-stream';
}

async function getOrCreateMonthFolder(drive, monthKey) {
  // Check known folders first
  if (MONTHLY_FOLDERS[monthKey]) {
    console.log(`Using known folder: ${monthKey} (${MONTHLY_FOLDERS[monthKey]})`);
    return MONTHLY_FOLDERS[monthKey];
  }

  // Search for existing folder
  const res = await drive.files.list({
    q: `name = '${monthKey}' and '${ARCHIVE_FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false`,
    fields: 'files(id, name)',
  });

  if (res.data.files.length > 0) {
    const folderId = res.data.files[0].id;
    console.log(`Found existing folder: ${monthKey} (${folderId})`);
    return folderId;
  }

  // Create new month folder
  console.log(`Creating new folder: ${monthKey}`);
  const folder = await drive.files.create({
    requestBody: {
      name: monthKey,
      mimeType: 'application/vnd.google-apps.folder',
      parents: [ARCHIVE_FOLDER_ID],
    },
    fields: 'id',
  });

  const newId = folder.data.id;
  console.log(`Created: ${monthKey} (${newId})`);
  return newId;
}

async function uploadVideo(videoPath, title) {
  if (!existsSync(videoPath)) {
    console.error(`File not found: ${videoPath}`);
    process.exit(1);
  }

  const fileName = title || basename(videoPath);
  const mimeType = getMimeType(videoPath);
  const monthKey = getCurrentMonthKey();

  console.log(`Uploading: ${fileName}`);
  console.log(`Target folder: Archive/${monthKey}`);

  // Auth via service account
  const keyPath = process.env.GOOGLE_SERVICE_ACCOUNT_KEY;
  if (!keyPath) {
    console.error('Set GOOGLE_SERVICE_ACCOUNT_KEY env var (path to service account JSON)');
    process.exit(1);
  }

  const auth = new google.auth.GoogleAuth({
    keyFile: keyPath,
    scopes: ['https://www.googleapis.com/auth/drive'],
  });

  const drive = google.drive({ version: 'v3', auth });
  const folderId = await getOrCreateMonthFolder(drive, monthKey);

  const fileContent = readFileSync(videoPath);
  const res = await drive.files.create({
    requestBody: {
      name: fileName,
      parents: [folderId],
    },
    media: {
      mimeType,
      body: fileContent,
    },
    fields: 'id, name, webViewLink',
  });

  console.log(`\n✓ Uploaded successfully`);
  console.log(`  Name: ${res.data.name}`);
  console.log(`  ID:   ${res.data.id}`);
  console.log(`  URL:  ${res.data.webViewLink}`);
  return res.data;
}

// CLI entry point
const [,, videoPath, title] = process.argv;
if (!videoPath) {
  console.error('Usage: node scripts/upload-to-archive.js <video_path> [title]');
  process.exit(1);
}

uploadVideo(videoPath, title).catch(err => {
  console.error('Upload failed:', err.message);
  process.exit(1);
});
