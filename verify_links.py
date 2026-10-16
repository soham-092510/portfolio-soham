import pymupdf

doc = pymupdf.open('Soham_Gaikwad_Resume.pdf')
print(f"Total Pages: {len(doc)}")
all_links = []
for pno in range(len(doc)):
    page = doc[pno]
    links = page.get_links()
    print(f"\n--- PAGE {pno+1} ({len(links)} links) ---")
    for l in links:
        uri = l.get('uri')
        rect = l.get('from')
        all_links.append(uri)
        print(f"  [{rect.x0:.1f}, {rect.y0:.1f}, {rect.x1:.1f}, {rect.y1:.1f}] -> {uri}")

print(f"\nTotal Links Found: {len(all_links)}")
