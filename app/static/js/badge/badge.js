
function createBadgeEl(badge) {
  return $(`
      <article class="media" id="badge-id-${badge.id}">
        <figure class="media-left">
          <p class="image is-64x64">
            <img src=${$SCRIPT_ROOT}/${badge.image_url}>
          </p>
        </figure>
        <div class="media-content">
          <div class="content">
            <p>
              <strong>${badge.name}</strong>
            </p>
          </div>
        </div>
      </article>
  `)
}

var deleteEl = $(`
        <div class="media-right">
          <button class="delete" id="delete-badge"></button>
        </div>
 `)

var badgeToRemove
var getDeleteBadgeCallback = (badgeId) => {
  return () => {
    badgeToRemove = badgeId
    $('#confirm-delete-badge').addClass("is-active")
  }
}
function listBadges() {
  var badgeListEl = $("#badge-list")

  $.get(`${$SCRIPT_ROOT}/badge/_get_badges`, (badges) => {
    console.log(badges)
    for (var badge of badges) {
      var badgeEl = createBadgeEl(badge)
      if (badge.id.indexOf('default') == -1) {
        badgeEl.append(deleteEl.clone())
        badgeEl.find('#delete-badge').click(getDeleteBadgeCallback(badge.id))
      }
      badgeListEl.append(badgeEl)
    }
  })
}

listBadges()

$('#cancel-removal').click(() => {
  $('#confirm-delete-badge').removeClass("is-active")
})

$('#confirm-removal').click(() => {
  var badgeEl = $(`#badge-id-${badgeToRemove}`)
  $.post(`${$SCRIPT_ROOT}/badge/_delete_badge?badge_id=${badgeToRemove}`, () => {
    badgeEl.remove()
    $('#confirm-delete-badge').removeClass("is-active")
  })
})