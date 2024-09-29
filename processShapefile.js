const fs = require('fs');
const shapefile = require('shapefile');
const iconv = require('iconv-lite');

async function decodeGBK(buffer) {
    // Decode GBK encoded buffer to UTF-8 string
    return iconv.decode(buffer, 'GBK');
}

async function processShapefile() {
    try {
        // Open the shapefile
        const source = await shapefile.open("C:/Users/r/Desktop/go-shp/shp/vegetation_china.shp");
        
        const filteredShapes = [];
        let count = 0;

        // Read each shape in the shapefile
        while (true) {
            const { value, done } = await source.read();
            if (done) break;

            const shape = value;

            // Read attribute values
            const attributes = shape.properties;

            // Check if the specific field exists (assuming it's the 10th field)
            const fieldKey = Object.keys(attributes)[9]; // Adjust index as necessary
            
            // Ensure the field is valid before decoding
            if (attributes[fieldKey] !== null && attributes[fieldKey] !== undefined) {
                const decodedVal = await decodeGBK(Buffer.from(attributes[fieldKey], 'binary')); // Decode the specific field value

                // Check if the decoded value matches desired criteria
                if (decodedVal === "草甸" || decodedVal === "草原" || decodedVal === "草丛") {
                    // Save the filtered shape
                    filteredShapes.push({ shape, attributes });
                    count++;
                }
            } else {
                console.warn(`Attribute at index ${fieldKey} is null or undefined, skipping.`);
            }
        }

        // Write the filtered shapes to a JSON file
        fs.writeFileSync("C:/Users/r/Desktop/js-shp/filtered_shapes.json", JSON.stringify(filteredShapes, null, 2));
        console.log(`Filtered shapes written: ${count}`);
    } catch (error) {
        console.error('Error processing shapefile:', error);
    }
}

// Run the process
processShapefile();
