function addToCart(id, name, price){
    event.preventDefault()

    fetch('/api/add-cart', {
        method:'POST',
        body: JSON.stringify({
            'id' : id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
     }).then(function(response){
            console.info(response)
            return response.json()
     }).then(function(data){
            console.info(data)

            let counter = document.getElementsByClassName('cart-counter')
            for(let i = 0; i < data.length; i++){
                counter[i].innerText = data.total_quantity
            }
     }).catch(function(error){
            console.error(error)
     })
}

function pay(){
       if(confirm('Ban chắc chắn thanh toán?')==true){
       fetch('/api/pay', {
            method:'POST',
     }).then(response => response.json()).then(data => {
        if(data.code == 200)
            location.reload()
     }).catch(error => console.error(error))
    }
}


function updateCart(id, obj){
    fetch('/api/update-cart',{
        method:'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value),
        }),
        headers:{
            'Content-Type': 'application/json'
        }
        }).then(respone => respone.json()).then(data =>{
            let counter = document.getElementsByClassName('cart-counter')
            for(let i = 0; i < data.length; i++)
                counter[i].innerText = data.total_quantity

            let amount = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}

function deleteCart(id){
    if(confirm("Bạn chắc chắn xóa sản phẩm này?")==true){
       fetch('/api/delete-cart/'+id, {
           method:'delete',
           headers: {
                'Content-Type': 'application/json'
                }
            }).then(response => response.json()).then(data => {
                let counter = document.getElementsByClassName('cart-counter');
                for(let i =0 ; i<counter.length();i++)
                    counter[i].innerText = data.total_quantity

                let amount = document.getElementById('total_amount');
                amount.innerText = new Intl.NumberFormat().format(data.total_amount)

                let e = document.getElementById("book" + id)
                e.style.display = "none"
            }).catch(error => console.error(error))
}
}


