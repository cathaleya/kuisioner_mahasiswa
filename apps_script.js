// ============================================================
// Google Apps Script — Penerima Data Instrumen PGSD
// Cara deploy:
//   1. Buka Google Sheet → Extensions → Apps Script
//   2. Paste kode ini, klik Save (💾)
//   3. Klik Deploy → New Deployment
//   4. Type: Web App
//   5. Execute as: Me
//   6. Who has access: Anyone
//   7. Deploy → Copy Web App URL
//   8. Paste URL ke APPS_SCRIPT_URL di kedua app.py
// ============================================================

function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var sheetName = payload.sheet;   // "Mahasiswa" atau "Dosen"
    var headers   = payload.headers; // array string header kolom
    var row       = payload.row;     // array nilai data

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var ws = ss.getSheetByName(sheetName);

    // Buat tab baru jika belum ada
    if (!ws) {
      ws = ss.insertSheet(sheetName);
    }

    // Tulis header jika sheet masih kosong
    if (ws.getLastRow() === 0) {
      ws.appendRow(headers);
      ws.getRange(1, 1, 1, headers.length)
        .setFontWeight("bold")
        .setBackground("#1e3a8a")
        .setFontColor("#ffffff");
      ws.setFrozenRows(1);
    }

    // Tambah baris data
    ws.appendRow(row);

    // Auto-resize kolom
    ws.autoResizeColumns(1, headers.length);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok", sheet: sheetName, row: ws.getLastRow() }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Fungsi test — jalankan manual untuk cek koneksi
function testDoPost() {
  var fakeEvent = {
    postData: {
      contents: JSON.stringify({
        sheet: "Test",
        headers: ["Timestamp", "Nama", "Skor"],
        row: [new Date().toISOString(), "Test User", 4.5]
      })
    }
  };
  var result = doPost(fakeEvent);
  Logger.log(result.getContent());
}
