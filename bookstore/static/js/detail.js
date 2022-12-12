
function addComment(bookId) {
    let content = document.getElementById('commentId').value
    if (content !== null || content.replace( /\s/g, '') !== '') {
        fetch('/api/comments', {

            method: 'post',
            body: JSON.stringify({
                'book_id': bookId,
                'content': content
            }),
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(res => res.json()).then(data => {
            if(data.status == 201) {
                let c = data.comment

                let area = document.getElementById('commentArea')

                area.innerHTML = `
                <hr>
                    <div class="row" style="font-size: 14px">
                        <div class="col-md-12">
                            <div style="padding-bottom: 6px; display: flex; align-items: center">
                                <img src="${c.user.avatar}"  width="30px" height="30px" class="img-fluid rounded-circle">
                                <span style="font-weight: 500; padding-left: 6px">${c.user.name}</span>
                             </div>
                            <p style="display: inline-block; width:30px"></p>

                            <div  style="display: inline-block;">
                                <p>${c.content}</p>
                                <p><em style="font-size: 11px">${moment(c.created_date).locale('vi').fromNow()}</em></p>
                            </div>
                        </div>
                    </div>
                ` + area.innerHTML
            } else if (data.status == 404)
                alert(data.err_msg)
        })
    }
    document.getElementById('commentId').value = ""



    
}