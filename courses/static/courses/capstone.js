document.addEventListener('DOMContentLoaded', function() {
    console.log("JS Active")

    btnEnroll();
    btnLike();
    btnEdit();
    btnEditUnit();
});

function btnEnroll() {
    document.querySelectorAll('.enroll').forEach(btn => {
        btn.onclick = function () {
            fetch('/enroll', {
                method: 'PUT',
                body: JSON.stringify({enroll: true, course_id: btn.dataset.id})
            })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    console.log(`Error at like: ${result.error}`);
                }
                else {
                    count = document.getElementById('enroll-count');
                    if (parseInt(result.enrolled) == 1) {
                        btn.textContent = "Unroll";
                        btn.classList.remove("btn-success");
                        btn.classList.add("btn-info");
                    } else {
                        btn.textContent = "Enroll Me";
                        btn.classList.remove("btn-info");
                        btn.classList.add("btn-success");
                    }
                    count.textContent = "Users enrolled: " +result.total;
                }
            });
        }
    });   
}

function btnLike() {
    document.querySelectorAll('.like').forEach(btn => {
        btn.onclick = function () {
            fetch('/like', {
                method: 'PUT',
                body: JSON.stringify({like: true, course_id: btn.dataset.id})
            })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    console.log(`Error at like: ${result.error}`);
                }
                else {
                    count = document.getElementById('likes-count');
                    if (parseInt(result.like) == 1) {
                        btn.textContent = "Unlike";
                        btn.classList.remove("btn-primary");
                        btn.classList.add("btn-warning");
                    } else {
                        btn.textContent = "Like";
                        btn.classList.remove("btn-warning");
                        btn.classList.add("btn-primary");
                    }
                    count.textContent = " Liked by: " +result.total;
                }
            });
        }
    });   
}

function btnEdit() {
    document.querySelectorAll('.edit').forEach(btn => {
        btn.onclick = function () {
            let title1 = document.querySelector(`#title`);
            let desc1 = document.querySelector(`#desc`);
            let img1 = document.querySelector(`#img`);
            title1.innerHTML = ` <form id="edit-course-form" class="card-text" style="margin-top: 1rem; margin-bottom: 1rem">
            <div class="form-group" style="margin-bottom: .7rem">
                <span style="font-size: 1rem">Title: </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-title">${title1.innerHTML}</textarea>

                    <span style="font-size: 1rem">Description: </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-desc">${desc1.innerHTML}</textarea>

                    <span style="font-size: 1rem">Image URL: </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-img">${img1.src}</textarea>
            </div>
            <input type="submit" class="btn btn-primary" value="Save"/>
            </form>`;

            document.querySelector('#edit-course-form').onsubmit = () => { 
                
                const title = document.querySelector('#edit-title').value;
                const desc = document.querySelector('#edit-desc').value;
                let img = document.querySelector('#edit-img').value;
                if (img == "") {
                    img = "https://es.talentlms.com/wp-content/uploads/2018/10/talentlms-content-library.png";
                }
                const course_id = btn.dataset.id;
                fetch('/edit', {
                    method: 'PUT',
                    body: JSON.stringify({course_id, title, desc, img})
                })
                .then(response => response.json())
                .then(result => {
                    if (result.error) {
                        console.log(`Error: ${result.error}`);
                    } else {
                        title1.innerHTML = title;
                        desc1.innerHTML = desc;
                        img1.src = img;
                    }
                })
                .catch(err => {
                    console.log(err)
                })
                return false;
            }
        }
    });
}

function btnEditUnit() {
    document.querySelectorAll('.edit-unit').forEach(btn => {
        btn.onclick = function () {
            let form = document.querySelector(`#unit-form`);
            let title1 = document.querySelector(`#title`);
            let desc1 = document.querySelector(`#desc`);
            let notes1 = document.querySelector(`#notes`);
            let vid1 = document.querySelector(`#vid`);
            let frame = document.querySelector(`#frame`);
            form.innerHTML = ` <form id="edit-unit-form" class="card-text" style="margin-top: 1rem; margin-bottom: 1rem">
            <div class="form-group" style="margin-bottom: .7rem">
                <span style="font-size: 1rem">Title: </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-title">${title1.textContent}</textarea>

                    <span style="font-size: 1rem">Description: </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-desc">${desc1.textContent}</textarea>

                    <span style="font-size: 1rem">Notes: </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-notes">${notes1.textContent}</textarea>

                    <span style="font-size: 1rem">Youtube URL (Put the last code or URL. Example: Tzl0ELY_TiM): </span><textarea 
                    style="overflow: hidden; resize: none"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                    class="form-control"
                    id="edit-vid">${vid1.textContent}</textarea>
            </div>
            <input type="submit" class="btn btn-primary" value="Save"/>
            </form>`;

            document.querySelector('#edit-unit-form').onsubmit = () => { 
                const title = document.querySelector('#edit-title').value;
                const desc = document.querySelector('#edit-desc').value;
                const notes = document.querySelector('#edit-notes').value;
                const vid = document.querySelector('#edit-vid').value;
                const unit_id = btn.dataset.id;
                
                fetch('/edit-unit', {
                    method: 'PUT',
                    body: JSON.stringify({unit_id, title, desc, notes, vid})
                })
                .then(response => response.json())
                .then(result => {
                    if (result.error) {
                        console.log(`Error: ${result.error}`);
                    } else {
                        form.innerHTML = '';
                        title1.innerHTML = title;
                        desc1.innerHTML = desc;
                        notes1.innerHTML = notes;
                        frame.src = `https://www.youtube.com/embed/${vid}`;
                    }
                })
                .catch(err => {
                    console.log(err)
                })

                return false;
            }
            
        }
    });
}