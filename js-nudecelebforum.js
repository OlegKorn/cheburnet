let a = document.querySelectorAll("[id^='post_message']")

arr_ = []

for (i=0; i<a.length; i++) {
    let links = a[i].querySelectorAll("a")
    
    for (j=0; j<links.length; j++) {
        link = links[j]["href"]
            arr_.push(link)        
    }
}
arr_
