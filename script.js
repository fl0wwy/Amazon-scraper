const jsonContainer = document.getElementById('json_container')
const request = new Request('data.json')

fetch(request)
    .then((Response) => Response.json())
    .then((data) => {
        console.log(data);
        for (let item in data) {
            const productDiv = document.createElement('div')
            productDiv.className = 'product'

            const img = document.createElement('img')
            img.id = 'product_img'
            img.src = data[item].img_src

            const content = document.createElement('div')
            content.className = 'content'

            const headline = document.createElement('h2')
            headline.id = 'product_name'
            headline.textContent = data[item].title

            const price = document.createElement('p')
            price.id = 'price'
            price.textContent = data[item].price

            const ratings = document.createElement('p')
            ratings.id = 'ratings'
            ratings.textContent = `${data[item].ratings[0]}, ${data[item].ratings[1]} reviews.`

            const link = document.createElement('a')
            link.id = 'product_link'
            link.href = data[item].product_link
            link.textContent = 'Amazon link'
            link.target = '_blank'

            content.appendChild(headline)
            content.appendChild(price)
            content.appendChild(ratings)
            content.appendChild(link)

            productDiv.appendChild(img)
            productDiv.appendChild(content)

            jsonContainer.appendChild(productDiv)    
        }
    })



