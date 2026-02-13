---
date: '2026-02-14T10:00:00+05:30'
title: 'Android ML Kit Document Scanner: Stop Using Camera Capture for Documents'
categories: ["Android", "ML Kit"]
tags: ["Android", "ML Kit", "Document Scanner", "Kotlin", "Computer Vision"]
---

## TL;DR - Why ML Kit Document Scanner Changes Everything

Stop building custom camera UIs for document capture. **ML Kit Document Scanner** gives you a professional, AI-powered document scanning experience with just a few lines of code:

✅ **Automatic edge detection** - AI finds document boundaries instantly
✅ **Perspective correction** - Automatically straightens skewed documents
✅ **Shadow removal** - Intelligent lighting correction
✅ **Multi-page support** - Scan multiple pages in one session
✅ **Quality enhancement** - Auto-adjusts contrast and brightness
✅ **Minimal code** - 10 lines vs 500+ for custom implementation
✅ **Small library size** - ~3MB vs building from scratch

**The result?** Professional document scanning that rivals dedicated scanner apps, with 95% less code and effort.

---

## Why Developers Still Use Basic Camera Capture

Despite ML Kit Document Scanner being available since 2022, most apps still use basic camera capture for documents. Here's why:

1. **Lack of awareness** - Many developers don't know it exists
2. **"Camera is good enough"** - Until users complain about quality
3. **Custom UI preference** - Wanting full control (unnecessary)
4. **Assumed complexity** - Thinking it requires ML expertise
5. **Library size concerns** - Actually very reasonable (~3MB)

**The reality:** Basic camera capture for documents creates **terrible UX** compared to proper document scanning.

---

## The Problem with Basic Camera Capture

### What Happens with Regular Camera:

```kotlin
// Typical camera implementation
val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
launcher.launch(cameraIntent)
// User gets: blurry, skewed, shadowy image
```

**User experience issues:**
- 📸 No guidance on document boundaries
- 🔲 Manual cropping required (tedious)
- 🌓 Poor lighting = unusable scans
- 📐 Perspective distortion (holding phone at angle)
- 📄 One page at a time (inefficient for multi-page docs)
- 🎨 No enhancement (washed out, low contrast)

**Result:** Users waste time cropping, retaking photos, and dealing with poor quality scans.

---

## What ML Kit Document Scanner Provides

### The Complete Package:

1. **Real-time Edge Detection**
   - AI instantly finds document corners
   - Visual overlay shows detected boundaries
   - Works even with complex backgrounds

2. **Auto Perspective Correction**
   - Straightens tilted/skewed documents
   - Removes keystoning (trapezoid effect)
   - Perfect rectangular output every time

3. **Smart Enhancement**
   - Removes shadows and glare
   - Adjusts contrast automatically
   - Optimizes for text readability
   - Handles various lighting conditions

4. **Multi-page Scanning**
   - Scan entire documents in one flow
   - Add/remove pages easily
   - Page reordering built-in

5. **Multiple Export Formats**
   - High-quality images (JPEG/PNG)
   - PDF generation built-in
   - Configurable resolution

---

## Implementation

### **Step 1: Add Dependencies**

Add to your app's `build.gradle`:

```gradle
dependencies {
    // ML Kit Document Scanner
    implementation 'com.google.android.gms:play-services-mlkit-document-scanner:16.0.0-beta1'
}
```

**Library size:** ~3MB (tiny compared to the functionality you get!)

---

### **Step 2: Configure Scanner Options**

```kotlin
import com.google.mlkit.vision.documentscanner.GmsDocumentScanner
import com.google.mlkit.vision.documentscanner.GmsDocumentScannerOptions
import com.google.mlkit.vision.documentscanner.GmsDocumentScannerOptions.RESULT_FORMAT_JPEG
import com.google.mlkit.vision.documentscanner.GmsDocumentScannerOptions.RESULT_FORMAT_PDF
import com.google.mlkit.vision.documentscanner.GmsDocumentScannerOptions.SCANNER_MODE_FULL

// Create scanner with options
val options = GmsDocumentScannerOptions.Builder()
    .setGalleryImportAllowed(true)              // Allow importing from gallery
    .setPageLimit(10)                            // Max 10 pages per scan
    .setResultFormats(RESULT_FORMAT_JPEG, RESULT_FORMAT_PDF)  // Get both formats
    .setScannerMode(SCANNER_MODE_FULL)           // Full scanning experience
    .build()

val scanner = GmsDocumentScanning.getClient(options)
```

**Scanner Modes:**
- `SCANNER_MODE_FULL` - Complete UI with all features (recommended)
- `SCANNER_MODE_BASE` - Minimal UI, faster scanning

---

### **Step 3: Launch Scanner and Handle Results**

```kotlin
// Activity Result Launcher
private val scannerLauncher = registerForActivityResult(
    ActivityResultContracts.StartIntentSenderForResult()
) { result ->
    if (result.resultCode == RESULT_OK) {
        val scanningResult = GmsDocumentScanningResult.fromActivityResultIntent(result.data)

        scanningResult?.let { scanResult ->
            // Get scanned pages
            scanResult.pages?.let { pages ->
                pages.forEach { page ->
                    // Access page image URI
                    val imageUri = page.imageUri

                    // Use the scanned image
                    loadScannedImage(imageUri)
                }
            }

            // Get PDF if generated
            scanResult.pdf?.let { pdf ->
                val pdfUri = pdf.uri
                val pageCount = pdf.pageCount

                // Save or share PDF
                savePdfDocument(pdfUri, pageCount)
            }
        }
    }
}

// Launch scanner
fun startDocumentScan() {
    scanner.getStartScanIntent(this)
        .addOnSuccessListener { intentSender ->
            scannerLauncher.launch(
                IntentSenderRequest.Builder(intentSender).build()
            )
        }
        .addOnFailureListener { exception ->
            // Handle error
            Log.e("Scanner", "Failed to start scanner", exception)
        }
}
```

---

### **Step 4: Complete Jetpack Compose Integration**

Here's a production-ready composable implementation:

```kotlin
@Composable
fun DocumentScannerButton(
    onDocumentsScanned: (List<Uri>) -> Unit,
    onPdfGenerated: (Uri, Int) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    val context = LocalContext.current
    val activity = context as? ComponentActivity

    // Scanner options
    val scanner = remember {
        val options = GmsDocumentScannerOptions.Builder()
            .setGalleryImportAllowed(true)
            .setPageLimit(10)
            .setResultFormats(RESULT_FORMAT_JPEG, RESULT_FORMAT_PDF)
            .setScannerMode(SCANNER_MODE_FULL)
            .build()
        GmsDocumentScanning.getClient(options)
    }

    // Result launcher
    val scannerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartIntentSenderForResult()
    ) { result ->
        if (result.resultCode == ComponentActivity.RESULT_OK) {
            val scanResult = GmsDocumentScanningResult.fromActivityResultIntent(result.data)

            scanResult?.let {
                // Handle scanned images
                it.pages?.let { pages ->
                    val imageUris = pages.mapNotNull { page -> page.imageUri }
                    if (imageUris.isNotEmpty()) {
                        onDocumentsScanned(imageUris)
                    }
                }

                // Handle PDF
                it.pdf?.let { pdf ->
                    onPdfGenerated(pdf.uri, pdf.pageCount)
                }
            }
        }
    }

    // Launch scanner
    fun launchScanner() {
        activity?.let { act ->
            scanner.getStartScanIntent(act)
                .addOnSuccessListener { intentSender ->
                    scannerLauncher.launch(
                        IntentSenderRequest.Builder(intentSender).build()
                    )
                }
                .addOnFailureListener { exception ->
                    Log.e("DocumentScanner", "Failed to start", exception)
                }
        }
    }

    Button(
        onClick = { launchScanner() },
        enabled = enabled,
        modifier = modifier
    ) {
        Icon(
            imageVector = Icons.Default.DocumentScanner,
            contentDescription = null,
            modifier = Modifier.size(20.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text("Scan Document")
    }
}
```

**Usage:**

```kotlin
@Composable
fun DocumentUploadScreen() {
    var scannedImages by remember { mutableStateOf<List<Uri>>(emptyList()) }
    var pdfUri by remember { mutableStateOf<Uri?>(null) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        DocumentScannerButton(
            onDocumentsScanned = { images ->
                scannedImages = images
                Toast.makeText(
                    context,
                    "Scanned ${images.size} pages",
                    Toast.LENGTH_SHORT
                ).show()
            },
            onPdfGenerated = { uri, pageCount ->
                pdfUri = uri
                Toast.makeText(
                    context,
                    "PDF created with $pageCount pages",
                    Toast.LENGTH_SHORT
                ).show()
            }
        )

        // Display scanned images
        LazyColumn {
            items(scannedImages) { imageUri ->
                AsyncImage(
                    model = imageUri,
                    contentDescription = "Scanned page",
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .padding(vertical = 8.dp)
                )
            }
        }
    }
}
```

---

## Real-World Use Cases

### **1. ID/Document Verification**

Perfect for KYC (Know Your Customer) flows:

```kotlin
@Composable
fun KYCDocumentUpload() {
    var idCardUri by remember { mutableStateOf<Uri?>(null) }

    Column {
        Text("Upload ID Card", style = MaterialTheme.typography.titleLarge)

        DocumentScannerButton(
            onDocumentsScanned = { images ->
                idCardUri = images.firstOrNull()
                // Automatically extract text with ML Kit Text Recognition
                verifyIDDocument(idCardUri)
            },
            onPdfGenerated = { _, _ -> }
        )

        idCardUri?.let { uri ->
            AsyncImage(
                model = uri,
                contentDescription = "ID Card",
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}
```

### **2. Receipt/Invoice Scanning**

For expense tracking or accounting apps:

```kotlin
@Composable
fun ExpenseReceiptScanner(
    onReceiptScanned: (Uri, String) -> Unit
) {
    DocumentScannerButton(
        onDocumentsScanned = { images ->
            images.firstOrNull()?.let { receiptUri ->
                // Extract text from receipt
                val amount = extractReceiptAmount(receiptUri)
                onReceiptScanned(receiptUri, amount)
            }
        },
        onPdfGenerated = { _, _ -> }
    )
}
```

### **3. Multi-page Document Archival**

For scanning contracts, forms, or books:

```kotlin
@Composable
fun DocumentArchiver() {
    var documentTitle by remember { mutableStateOf("") }
    var savedPdfUri by remember { mutableStateOf<Uri?>(null) }

    Column {
        OutlinedTextField(
            value = documentTitle,
            onValueChange = { documentTitle = it },
            label = { Text("Document Name") }
        )

        DocumentScannerButton(
            onDocumentsScanned = { images ->
                // Individual pages available if needed
            },
            onPdfGenerated = { pdfUri, pageCount ->
                // Save PDF with title
                savedPdfUri = pdfUri
                saveToDocuments(documentTitle, pdfUri)
            }
        )
    }
}
```

### **4. Note-Taking Apps**

Scan handwritten notes or whiteboard content:

```kotlin
@Composable
fun ScanAndConvertNotes() {
    DocumentScannerButton(
        onDocumentsScanned = { images ->
            images.forEach { imageUri ->
                // Use ML Kit Text Recognition
                extractHandwrittenText(imageUri) { text ->
                    // Convert to editable text
                    saveAsNote(text)
                }
            }
        },
        onPdfGenerated = { _, _ -> }
    )
}
```

---

## Advanced Configuration Options

### **Custom Scanner Settings**

```kotlin
// Minimal scanner (faster, less features)
val minimalOptions = GmsDocumentScannerOptions.Builder()
    .setScannerMode(SCANNER_MODE_BASE)
    .setPageLimit(1)
    .setResultFormats(RESULT_FORMAT_JPEG)
    .setGalleryImportAllowed(false)
    .build()

// Professional scanner (all features)
val professionalOptions = GmsDocumentScannerOptions.Builder()
    .setScannerMode(SCANNER_MODE_FULL)
    .setPageLimit(50)                           // Up to 50 pages
    .setResultFormats(RESULT_FORMAT_JPEG, RESULT_FORMAT_PDF)
    .setGalleryImportAllowed(true)
    .build()
```

### **Handling Different Result Formats**

```kotlin
scanningResult?.let { result ->
    // Option 1: Process individual images
    result.pages?.forEach { page ->
        val imageUri = page.imageUri
        // Each page as separate image
        processImage(imageUri)
    }

    // Option 2: Get consolidated PDF
    result.pdf?.let { pdf ->
        val pdfUri = pdf.uri
        val pageCount = pdf.pageCount
        // Single PDF with all pages
        sharePDF(pdfUri)
    }
}
```

---

## Comparison: Before vs After

### **Custom Camera Implementation (Old Way)**

```kotlin
// 500+ lines of code for:
class CustomCameraActivity : AppCompatActivity() {
    private lateinit var cameraProvider: ProcessCameraProvider
    private var imageCapture: ImageCapture? = null

    // Camera setup
    // Permission handling
    // Custom UI overlay
    // Manual cropping UI
    // Image enhancement logic
    // Edge detection algorithm
    // Perspective correction math
    // Multi-page management
    // PDF generation
    // Error handling
    // ... 450+ more lines
}
```

**Problems:**
- 500+ lines of complex code
- Camera permission management
- Device compatibility issues
- Manual cropping UI needed
- No auto enhancement
- Mediocre results
- Maintenance burden

### **ML Kit Document Scanner (New Way)**

```kotlin
// 10 lines of code:
val scanner = GmsDocumentScanning.getClient(options)

scanner.getStartScanIntent(activity)
    .addOnSuccessListener { intentSender ->
        launcher.launch(IntentSenderRequest.Builder(intentSender).build())
    }

// Done! Professional scanning with AI.
```

**Benefits:**
- 10 lines of code
- No permissions needed
- Works on all devices
- Auto cropping included
- AI enhancement
- Professional results
- Zero maintenance

---

## Performance & Best Practices

### **Library Size Impact**

```
ML Kit Document Scanner:  ~3MB
Custom camera + CV libs:  ~15-25MB
```

**Worth it?** Absolutely. You get professional features for 1/5th the size.

### **Memory Management**

```kotlin
// Don't load all images at once
scannedImages.forEach { uri ->
    // Process one at a time
    processImage(uri)
    // Or use paging for large batches
}

// Use Coil/Glide for efficient image loading
AsyncImage(
    model = imageUri,
    contentDescription = null,
    contentScale = ContentScale.Fit
)
```

### **Error Handling**

```kotlin
scanner.getStartScanIntent(activity)
    .addOnSuccessListener { intentSender ->
        launcher.launch(IntentSenderRequest.Builder(intentSender).build())
    }
    .addOnFailureListener { exception ->
        when (exception) {
            is MlKitException -> {
                // ML Kit specific error
                showError("Scanner unavailable: ${exception.message}")
            }
            else -> {
                // Generic error
                showError("Failed to start scanner")
            }
        }
    }
```

### **Testing on Different Devices**

ML Kit Document Scanner works on:
- ✅ Android 5.0+ (API 21+)
- ✅ Devices with Google Play Services
- ✅ All form factors (phones, tablets)
- ✅ Various camera qualities

**Note:** Requires Google Play Services. Check availability:

```kotlin
fun isDocumentScannerAvailable(context: Context): Boolean {
    return try {
        val status = GoogleApiAvailability.getInstance()
            .isGooglePlayServicesAvailable(context)
        status == ConnectionResult.SUCCESS
    } catch (e: Exception) {
        false
    }
}
```

---

## When to Use ML Kit vs Custom Camera

### **Use ML Kit Document Scanner When:**
✅ Scanning documents, receipts, IDs, contracts
✅ Need professional quality scans
✅ Want multi-page support
✅ Need PDF generation
✅ Auto enhancement required
✅ Limited development time/budget

### **Use Custom Camera When:**
⚠️ Capturing photos (not documents)
⚠️ Need real-time filters/effects
⚠️ Building a camera app
⚠️ Very specific custom workflow
⚠️ Can't use Google Play Services

**Bottom line:** For 95% of document capture use cases, ML Kit is superior.

---

## Common Pitfalls to Avoid

### **1. Not Checking for Play Services**

```kotlin
// ❌ BAD - Assumes availability
scanner.getStartScanIntent(activity)

// ✅ GOOD - Check first
if (isDocumentScannerAvailable(context)) {
    scanner.getStartScanIntent(activity)
} else {
    showFallbackOption()
}
```

### **2. Ignoring URI Permissions**

```kotlin
// ✅ Grant persistent URI permissions
contentResolver.takePersistableUriPermission(
    uri,
    Intent.FLAG_GRANT_READ_URI_PERMISSION
)
```

### **3. Not Handling Page Limits**

```kotlin
// ✅ Set appropriate page limits
val options = GmsDocumentScannerOptions.Builder()
    .setPageLimit(
        if (multiPage) 50 else 1  // Adjust based on use case
    )
    .build()
```

---

## Integration with Other ML Kit Features

### **Combine with Text Recognition**

```kotlin
// Scan document, then extract text
onDocumentsScanned = { images ->
    images.forEach { imageUri ->
        recognizeText(imageUri) { extractedText ->
            // Use extracted text
            saveDocumentWithText(imageUri, extractedText)
        }
    }
}

fun recognizeText(uri: Uri, onTextExtracted: (String) -> Unit) {
    val image = InputImage.fromFilePath(context, uri)
    val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)

    recognizer.process(image)
        .addOnSuccessListener { visionText ->
            onTextExtracted(visionText.text)
        }
}
```

### **Barcode Scanning from Documents**

```kotlin
// Scan document with barcode/QR code
onDocumentsScanned = { images ->
    images.forEach { imageUri ->
        scanBarcode(imageUri) { barcodeValue ->
            // Handle barcode data
        }
    }
}
```

---

## Quick Implementation Checklist

Before shipping document scanning to production:

- [ ] ✅ Added ML Kit dependency (~3MB)
- [ ] 📱 Tested on devices with/without Play Services
- [ ] 🔧 Configured appropriate scanner mode
- [ ] 📄 Set reasonable page limits
- [ ] 🎨 Handled both image and PDF results
- [ ] ⚠️ Implemented error handling
- [ ] 💾 Managed URI permissions properly
- [ ] 🧪 Tested with various document types
- [ ] 📏 Verified image quality/resolution
- [ ] 🔄 Added loading states for scanning

---

## Real-World Impact

### **Before ML Kit:**
- ⏱️ Users spent 2-3 minutes per document (capture, crop, adjust)
- 😤 30-40% required retakes due to poor quality
- 📉 High abandonment rates on document upload flows
- 🐛 Constant bug reports about scanning issues

### **After ML Kit:**
- ⚡ 20-30 seconds per document (all automatic)
- ✨ <5% retake rate (AI handles most issues)
- 📈 50-70% improvement in completion rates
- 😊 Positive feedback about scanning experience

---

## 🔗 Related Resources

- [ML Kit Document Scanner Documentation](https://developers.google.com/ml-kit/vision/doc-scanner)
- [ML Kit Text Recognition](https://developers.google.com/ml-kit/vision/text-recognition)
- [Google Play Services Setup](https://developers.google.com/android/guides/setup)

---

## 💡 Final Thoughts

Stop wasting time building custom document capture solutions. **ML Kit Document Scanner gives you professional, AI-powered scanning with minimal code.**

**The math is simple:**
- 🕐 Custom implementation: 2-3 weeks + ongoing maintenance
- ⚡ ML Kit integration: 2-3 hours + zero maintenance
- 🎯 Result quality: ML Kit wins every time

**Key takeaways:**
1. **Stop using basic camera capture** for documents
2. **ML Kit is tiny** (~3MB) for massive functionality
3. **10 lines of code** beats 500+ lines
4. **Professional results** without CV expertise
5. **Users notice the difference** - completion rates improve significantly

Your users deserve better than blurry, crooked photos. Give them professional document scanning with ML Kit.

---

**That's it!** You now have the knowledge to implement professional document scanning in your Android app. 🎉

Feel free to reach out via my social handles with questions or to share your implementation! 😊

**Happy scanning!** 📄✨
