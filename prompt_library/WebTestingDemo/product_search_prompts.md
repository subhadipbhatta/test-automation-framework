# Product Search Prompts Library

## Search Functionality Prompts

### Prompt: SEARCH_001_Keyword_Search
```
Test product search using specific keywords.

**Test Keywords:**
- "computer"
- "book"
- "jewelry"
- "electronics"

**Steps:**
1. Navigate to homepage (https://demowebshop.tricentis.com/)
2. Locate search box in header
3. Enter keyword: {keyword}
4. Click search button or press Enter
5. Review search results page
6. Verify search results relevance

**Expected Results:**
- Relevant products displayed
- Search results contain keyword in title or description
- Product count shown
- Search term highlighted in results
- Filtering options available on results page
```

### Prompt: SEARCH_002_Category_Browse
```
Test product browsing by category navigation.

**Categories to Test:**
- Books
- Computers
- Electronics
- Apparel & Shoes
- Digital downloads
- Jewelry
- Gift Cards

**Steps:**
1. Navigate to homepage
2. Locate main navigation menu
3. Click on category: {category}
4. Wait for category page to load
5. Browse category product listings
6. Verify category-specific content

**Expected Results:**
- Category page loads correctly
- Products in selected category displayed
- Category name shown in page title/breadcrumb
- Category-specific filters available
- Subcategories displayed if applicable
```

### Prompt: SEARCH_003_Price_Filter
```
Test product filtering by price range.

**Test Data:**
- Minimum price: {minPrice}
- Maximum price: {maxPrice}

**Steps:**
1. Navigate to a product category page
2. Locate price filter controls
3. Set minimum price: {minPrice}
4. Set maximum price: {maxPrice}
5. Apply price filter
6. Review filtered results

**Expected Results:**
- Products filtered by specified price range
- All displayed products within price range
- Filter controls update correctly
- Product count reflects applied filter
- Filter can be cleared/reset
```

### Prompt: SEARCH_004_Sort_Products
```
Test product sorting functionality on category/search pages.

**Sorting Options to Test:**
- Name: A to Z
- Name: Z to A
- Price: Low to High
- Price: High to Low
- Created On (if available)

**Steps:**
1. Navigate to product listing page (category or search results)
2. Locate sort dropdown/controls
3. Select sort option: {sortOption}
4. Wait for page to reload/update
5. Verify sorting is applied correctly

**Expected Results:**
- Products reordered according to selected sort
- Sort option reflected in UI
- Sorting maintained during pagination
- All products follow selected sort criteria
```

### Prompt: SEARCH_005_Advanced_Search
```
Test advanced search functionality if available.

**Advanced Search Criteria:**
- Category selection
- Price range
- Manufacturer/Brand (if applicable)
- Keywords

**Steps:**
1. Navigate to homepage
2. Look for advanced search link/option
3. Access advanced search form
4. Fill in multiple search criteria
5. Execute advanced search
6. Review combined filter results

**Expected Results:**
- Advanced search form accessible
- Multiple criteria can be combined
- Search results respect all applied filters
- Results accurately match all criteria
- Clear way to modify or reset criteria
```

### Prompt: SEARCH_006_Empty_Search_Results
```
Test search behavior with no matching results.

**Test Scenarios:**
- Search for non-existent product: "zzzznonexistent"
- Search with very specific criteria that yields no results

**Steps:**
1. Navigate to homepage
2. Enter search term that will yield no results
3. Execute search
4. Verify no results handling
5. Check for search suggestions or alternatives

**Expected Results:**
- No results page displayed appropriately
- Clear message that no products found
- Suggestions for alternative searches (if available)
- Option to clear search or browse categories
- Search form remains functional for new search
```