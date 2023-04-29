document.addEventListener('DOMContentLoaded', (event) => {

    var dragSrcEl = null;
    
    function handleDragStart(e) {
        this.style.opacity = '0.4';
      
        dragSrcEl = this;
  
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.innerHTML);
    }
  
    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();
        }
  
        e.dataTransfer.dropEffect = 'move';
      
        return false;
    }
  
    function handleDragEnter(e) {
        this.classList.add('over');
    }
  
    function handleDragLeave(e) {
        this.classList.remove('over');
    }
  
    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation(); // stops the browser from redirecting.
        }
        
        if (dragSrcEl != this) {
            dragSrcEl.innerHTML = this.innerHTML;
            this.innerHTML = e.dataTransfer.getData('text/html');
        }
        
        return false;
    }      
  
    function handleDragEnd(e) {
        this.style.opacity = '1';
      
        items.forEach(function (item) {
            item.classList.remove('over');
        });
    }
    
    
    let items = document.querySelectorAll('.grid .grid-item');
    items.forEach(function(item) {
        item.addEventListener('dragstart', handleDragStart, false);
        item.addEventListener('dragenter', handleDragEnter, false);
        item.addEventListener('dragover', handleDragOver, false);
        item.addEventListener('dragleave', handleDragLeave, false);
        item.addEventListener('drop', handleDrop, false);
        item.addEventListener('dragend', handleDragEnd, false);
    });
});

function saveData(){
    // get the data from the grid (without the tags) items and call the web api to save the data
    let items = document.querySelectorAll('.grid .grid-item');
    let data = [];
    items.forEach(function(item) {
        // get the name without tags
        let name = item.innerHTML;
        data.push({id: item.id, value: item.innerHTML});
    });

    // Send the data to the server to save it, you need to use fetch and the api is /api/voorkeur/leerling/.
    fetch('/api/voorkeur/desktop/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })

    // redirect to the next page
    window.location.href = '/bedankt';
}