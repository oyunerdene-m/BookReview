const template = Handlebars.compile(document.querySelector('#result').innerHTML);

document.addEventListener('DOMContentLoaded', () => {
  const u = document.location.href.split('/');
  const id = u[u.length-1]; 

  ///show reviews
  document.querySelector('#reviews-button').onclick = () => {
    event.preventDefault();

    fetch(`/api/book/reviews/${id}`)
      .then(response => response.json())
      .then(data => {
        const content = template({'reviews': data['reviews']});
        document.querySelector('#reviews').innerHTML = content;
      });
  }

  ///add review
  document.querySelector('#add-form').onsubmit = () => {
    event.preventDefault()
  
    const formData = new FormData();
    const content = document.querySelector('#content').value;
    const rating = document.querySelector('#rating').value;
    formData.append('content', content);
    formData.append('rating', rating);
    
    fetch(`/api/review/new/${id}`, {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(result => {
      const content = template({'reviews': [result['review']]});
      document.querySelector('#reviews').innerHTML += content;
      document.querySelector('#content').value = '';
      document.querySelector('#rating').value = '';
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
})