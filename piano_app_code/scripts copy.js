document.addEventListener('DOMContentLoaded', () => {

    // Show/hide error message
    const showVoteErrorMsg = (msg, id) => {
        const msgDiv = document.querySelector(`.vote-msg[data-piano="${id}"]`);
        msgDiv.textContent = msg;
        msgDiv.style.display = "block";

        setTimeout(() => {
            msgDiv.style.display = "none";
        }, 2500)
    }
   
    // Vote for piano function
    // Assign event listener for every entry of class
    document.querySelectorAll('.vote-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        
        // Assign piano data attribute value to variable
        const pianoId = btn.dataset.piano;

        // This token is usually hidden
        const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;
        
        // For testing only
        console.log("Voting for " + pianoId);

        // Contacting API located at address in urls.py file
        const response = await fetch(`/pianos/vote/${pianoId}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: 1
            }),
            headers: {
                "X-CSRFToken": token,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Failed to vote")
        }

        // Convert json object to JS object
        const data = await response.json();

        // If JS object key = 'msg', call error function
        if (data.msg) {
            console.log(data.msg)
            showVoteErrorMsg(data.msg, pianoId);
        } 
        else {
        // Display content
            console.log(data.content);
            // Adding returned content to the page by accessing the JS object 'content' property
            document.querySelector(`.piano-votes[data-piano="${pianoId}"]`).textContent = `Number of votes: ${data.content}`
        }
    });
   });


   // Delete piano

    const deleteLinks = document.querySelectorAll('.piano_delete_links');
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    // const pianoIndexUrl = "{% url 'index' %}";

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const confirmation = confirm("Are you really sure you want to delete this wonderful piano?")

            if (confirmation) {
                // Get the URL from the dataset
                const url = this.dataset.url;
                // Find the parent card element
                const pianoCard = this.closest('.card.mb-3');

                fetch (url, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json'
                    },
                }).then(response => {
                    if (response.ok) {
                        alert('Piano has been successfully deleted.');
                        // Remove the card element from the DOM
                        pianoCard.remove();
                    } else {
                        alert("Houston, we have a problem.")
                    }
                }).catch(err => console.error("Error", err))
            }
        })
    })

});
// End DOMContentLoaded

