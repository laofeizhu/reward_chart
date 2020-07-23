function createChildEl(child) {
  return $(`
      <article class="media" id="child-id-${child.id}">
        <a href=${$SCRIPT_ROOT}/chart/index?child_id=${child.id}>
          <figure class="media-left">
            <p class="image is-64x64">
              <img src=${$SCRIPT_ROOT}/file/${child.avatar_url}>
            </p>
          </figure>
        </a>
        <div class="media-content">
          <div class="content">
            <p>
              <a href=${$SCRIPT_ROOT}/chart/index?child_id=${child.id}>
                <strong>${child.name}</strong>
              </a>
              <br>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare magna eros, eu pellentesque tortor vestibulum ut. Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.
            </p>
          </div>
        </div>
        <div class="media-right">
          <button class="delete" id="delete-child"></button>
        </div>
      </article>
  `)
}

var childToRemove

var getDeleteChildCallback = (childId) => {
  return () => {
    childToRemove = childId
    $('#confirm-delete-child').addClass("is-active")
  }
}

function listChildren() {
  var childListEl = $("#child-list")

  $.get(`${$SCRIPT_ROOT}/family/_get_children`, (children) => {
    for (var child of children) {
      var childEl = createChildEl(child)
      childListEl.append(childEl)
      childEl.find('#delete-child').click(getDeleteChildCallback(child.id))
    }
  })
}

listChildren()

$('#cancel-removal').click(() => {
  $('#confirm-delete-child').removeClass("is-active")
})

$('#confirm-removal').click(() => {
  var childEl = $(`#child-id-${childToRemove}`)
  $.post(`${$SCRIPT_ROOT}/family/_delete_child?child_id=${childToRemove}`, ()=>{
    childEl.remove()
    $('#confirm-delete-child').removeClass("is-active")
  })
})