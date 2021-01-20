# Detailed Project Notes


## Resources 
- https://cloud.google.com/vision/docs/fulltext-annotations
- https://cloud.google.com/vision/docs/ocr
- https://cloud.google.com/vision/docs/detecting-fulltext
- https://cloud.google.com/vision/docs/detecting-text#vision-text-detection-python
- https://cloud.google.com/vision/docs/quickstart-client-libraries


## Goals (in order of increasing complexity): 
1. Extract the ingredients in one block of text given a photo of just the ingredients or of just the ingredients and a very small area of the packaging around them. 
2. Extract the ingredients in one block given a photo of the whole side of the packaging (quite difficult!) 
3. Extract various logos showing product certifications etc. Note that this can be done as an object detection task on all of them at the same time and can be done with video in real time (tf object detection supports video). 



## OCR on the whole package 
- We first try to use the Google Vision API (both the text and document detection options) to segment the text from the whole side of the package. The hope is that this provides a good segmentation and from there we can extract the blocks we need (i.e. ingredients and nutrition) easily, e.g. by keyword search for 'ingredients' and 'nutrition' in the various blocks. 
- Experimenting with various package designs shows that the out-of-the-box Google Vision API (document, as this one is better) doesn't capture a lot of the cases well. For example, it thinks that pargraphs are supposed to be horizontal and groups horizontal text together even when the left and right hand side of it come from different columns. Conclusion is that this is too crude to be useful out-of-the-box. 
- We might need to go back to first principles and group words together based on the distance between their bounding boxes in all directions, rather than relying on the paragraph-level segmentation that comes out of the API. 
- There is a first attempt - a fuction to merge bounding boxes together well; however this is WIP. Probably need to do the following: define min distances between sizes of the bboxes and only merge if these distances are below a certain threshold. Potential challenges: having different styles, fonts, spacing, layout can make it hard to define a min distance. 
- See various attempts and comments in the OCR_packaging_workbook notebook. 


## Issues
- [1] Using block detection with the Vision API out of the box doesn't detect columns well and groups together things which are supposed to be in different blocks.
- [2] It's not perfect with numbers and this can be a problem with the nutrition info; sometimes it separates just a few numbers from the rest of the block or paragraph  and sometimes it doesn't even detect them correctly e.g. the letter 'g' or '.' 
- [3] Even with block and paragraph detection, sometimes it picks up small individual blocks of e.g. just one number or word and this gets taken out of the bigger block that encloses it.
- [4] Lots of packages are round or the photos are distorted and when that happens it's not good at putting proper boxes around groups of text and this instead gets chopped into really bad boxes; or the text is not extracted very well. 
- [5] For ingredients: depending on the layout sometimes it doesn't detect the word 'ingredients' together with the actual ingredient list, or splits the ingredients in two or more blocks; or puts more stuff into the box that contains the ingredients. 
- [6] Sometimes the word 'ingredients' doesn't get fully detected esp when the package is distorted. 
- [7] For the nutrition: A lot of issues in correctly extracting this information. 
- [8] Sometimes the word 'ingredients' is contained elsewhere in the text and not with the actual ingredients list. 
- [9] Sometimes ingredients are not neatly separated by commas or there is no fullstop at the end. 
- [10] Even when we successully extract the ingredients list, there are issues such as text in brackets separated over multiple lines being split or unconventional formatting.


## Solutions

Solution 1
- *Defintion*: Instead of using the block and document functionality of the API, use just the words and their bounding boxes and group them together based on distances. 
- *Challenges*: Probably no perfect way to determine what the optimal distance is between words as the layouts are very different; e.g. adding spacing for style reasons. 
- *Solution*: Compute all distances between words and define min distances based on which they are grouped into a cluster. 
- *Applicable to*: [1]

Solution 2 
- *Defintion*: Try to merge overlapping blocks to address the issue of random single words or numbers being picked as a separate block within the blocks. 
- *Challenges*: Might slow down the computation quite a lot. How do we make sure that the words are placed in the right place in the bigger block? 
- *Solution*: Use blocks merging with non-max supression and extract block coordinates this way; then combine the text within these blocks. 
- *Applicable to*: [3]

Solution 3 
- *Deifntion*: Flatten round and creased packages. 
- *Challenegs*: Don't know how to do this at the moment; I believe that solutions exist but not sure how good or efficient they are. 
- *Solution*: Use image flattening algorithm. 
- *Applicable to*: [4]

Solution 4 
- *Definition*: Use partial string matching to get the ingredients info instread of just looking for the word 'ingredients'.
- *Challenges*: Need to be done in a way that doesn't increase the compute time. 
- *Solution*: Partial string matching.
- *Applicable to*: [6]

Solution 5 
- *Definition*: Merging and cleaning all the nutrition info together. 
- *Challenegs*: Hard to think of all the exceptions that will occur; will also slow us down. 
- *Solution*: After detecting the word 'ingredients' and the block to which it belongs, find the block size and if this is below a given threshold i.e. if there is probably nothing or not much grouped in the same block, get also the text from the next block and merge these together; Add other conditions for splitting the ingredients so as to eliminate text that comes after the end of the actual ingredients list - looking for fullstop and lack of comma separated text following that. 
- *Applicable to*: [5], [9]

Solution 6 
- *Definition*: Look for all the occurrences of the word 'ingredients' instead of just the first one, which sometimes is not where the actual ingredients list starts. 
- *Challenges*: Instead of looking at a single block we now need to look at multiple and impose conditions, which slows us down. 
- *Solution*: Apply the pipeline to all the blocks containing the word 'ingredients' and merge the output at the end. 
- *Applicable to*: [9]


Solution 7 
- *Defintion*: Cleaning of the outcome for the ingredients list. 
- *Challenegs*: Too many exceptions. What does a 'clean list of ingredients' look like? 
- *Solution*: Introduce various text cleanining based on dataset and trial and error. 
- *Applicable to*: [10]
