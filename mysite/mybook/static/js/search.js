const template = Handlebars.compile(document.querySelector('#result').innerHTML);

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#form').onsubmit = () => {
    event.preventDefault()

    const search = document.querySelector('#search').value;

    fetch('/api/books/search?search=' + search)
      .then(response => response.json())
      .then(data => {
        if(data.success){
        const content = template({'books': data['books']});
        document.querySelector('#search_result').innerHTML = content;
        } else {
          document.querySelector('#search_result').innerHTML = "<div class='alert alert-warning' role='alert'>Book doesn't exist!</div>"
        }
      });
  };
})