# Product Details Prompts Library

## Product Information Validation Prompts

### Prompt: PRODUCT_001_Detail_Page_Navigation
```
Test navigation to product detail page and information validation.

**Product Selection Criteria:**
- Select first available product from search results
- Or select specific product: {productName}

**Steps:**
1. Navigate to product listing page (category or search)
2. Click on product title or image: {productName}
3. Wait for product detail page to load
4. Validate all product information elements are present
5. Verify page layout and content

**Elements to Validate:**
- Product title
- Product price (clear and visible)
- Product description
- Product images
- Stock availability status
- Add to Cart button
- Product reviews/ratings (if available)
- Product specifications

**Expected Results:**
- Product detail page loads completely
- All information displayed correctly
- Images load properly and are relevant
- Price format is correct and clear
- Add to Cart button is functional and visible
- Product URL contains product identifier
```

### Prompt: PRODUCT_002_Image_Gallery_Validation
```
Test product image gallery functionality.

**Steps:**
1. Navigate to product detail page with multiple images
2. Locate product image gallery/carousel
3. Test image navigation controls
4. Test image zoom functionality (if available)
5. Validate image quality and loading
6. Test image thumbnail navigation

**Expected Results:**
- All product images load correctly
- Image navigation works smoothly (next/previous)
- Thumbnail images function properly
- Zoom functionality operates if available
- Images are high quality and show product clearly
- Main image updates when thumbnails are clicked
```

### Prompt: PRODUCT_003_Price_Validation
```
Test price display and formatting across multiple products.

**Steps:**
1. Navigate to different product categories
2. Select 3-5 products for price validation
3. Record product names and displayed prices
4. Compare price formats and currency display
5. Verify price consistency across the site

**Expected Results:**
- All prices displayed in consistent format
- Currency symbols correct and consistent
- Price decimal places consistent
- No pricing errors or formatting issues
- Special pricing (sales, discounts) clearly marked
```

### Prompt: PRODUCT_004_Add_To_Cart_Validation
```
Test "Add to Cart" functionality from product detail page.

**Test Product:**
- Product: {productName}
- Quantity: 1 (default)

**Steps:**
1. Navigate to product detail page: {productName}
2. Verify default quantity is set to 1
3. Click "Add to Cart" button
4. Verify cart update notification/confirmation
5. Check cart counter/badge update
6. Navigate to cart page to verify item added

**Expected Results:**
- Add to Cart button is clearly visible and functional
- Cart update notification appears
- Cart counter updates to show new item count
- Product correctly added to cart with right details
- Cart page shows added product with correct information
```

### Prompt: PRODUCT_005_Product_Specifications
```
Test product specification display and completeness.

**Steps:**
1. Navigate to product detail page for technical product
2. Locate product specifications section
3. Verify specification details are comprehensive
4. Check specification formatting and organization
5. Verify technical details accuracy

**Expected Results:**
- Product specifications clearly organized
- Technical details provided where relevant
- Specifications easy to read and understand
- No missing or placeholder specification data
- Specifications match product title and description
```

### Prompt: PRODUCT_006_Related_Products
```
Test related products or recommendations display.

**Steps:**
1. Navigate to product detail page
2. Scroll to find related/recommended products section
3. Verify related products are relevant
4. Test clicking on related product links
5. Verify related products lead to correct detail pages

**Expected Results:**
- Related products section displays if available
- Recommended products are relevant to current product
- Related product links function correctly
- Related products have consistent information display
- Navigation between related products works smoothly
```

### Prompt: PRODUCT_007_Stock_Availability
```
Test product stock status and availability display.

**Steps:**
1. Navigate to various product detail pages
2. Check stock availability information
3. Verify stock status messaging
4. Test behavior for out-of-stock items (if any)
5. Verify stock information is clear and accurate

**Expected Results:**
- Stock availability clearly displayed
- In-stock items show available status
- Out-of-stock items handled appropriately
- Stock messaging is clear and understandable
- Add to Cart button behavior matches stock status
```