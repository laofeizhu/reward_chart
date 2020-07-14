var dayEntry = $(`
<article class="post chart-row">
  <h4 class="chart-date"></h4>
  <div class="score-box field is-grouped is-grouped-multiline"></div>
</article>
`)

for (var i = 0; i < 7; ++i) {
  $('#chart-body').append(dayEntry.clone())
}

var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
var dateField = $('.chart-date')
var oneDay = 24 * 3600 * 1000
var oneHour = 3600 * 1000
var oneMin = 60 * 1000
var oneSec = 1000

var now = new Date()
var nowSec = now.getTime()
var lastSundaySec
var stars
var starsLeft

function updateTime() {
  let oldLastSundaySec = lastSundaySec
  lastSundaySec = nowSec - oneDay * now.getDay() - oneHour * now.getHours() - oneMin * now.getMinutes() - oneSec * now.getSeconds()
  for (var i = 0; i < 7; ++i) {
    var d = new Date(lastSundaySec + i * oneDay)
    dateField[i].innerHTML = '(' + (d.getMonth() + 1) + '/' + d.getDate() + ') ' + DAYS[i]
  }
  for (var i = 0; i < 7; ++i) {
    $('.chart-row').eq(i).removeClass('has-background-primary')
  }

  $('.chart-row').eq(now.getDay()).addClass('has-background-primary')
  if (oldLastSundaySec !== lastSundaySec) {
    updateScores()
  }
}

// do a time update immediately
updateTime()

setInterval(() => {
  now = new Date()
  nowSec = now.getTime()
  updateTime()
}, 5000)

var addStarModal = $('#add-star-modal')

function createBadgeEl(image_url) {
  return $(`<div><figure class="image is-64x64">
  <img src=${$SCRIPT_ROOT}/file/${image_url}>
</figure></div>`)
}

function showBadgesToAdd() {
  $.get($SCRIPT_ROOT + '/badge/_get_badges_for_child/' + $CHILD_ID, function(badges) {
    for (let badge of badges) {
      var badgeEl = createBadgeEl(badge.image_url)
      badgeEl.click(() => {
        // add to earlier days if earlier days are selected
        $.post(`${$SCRIPT_ROOT}/badge/_score?child_id=${$CHILD_ID}&badge_id=${badge.id}&timestamp=${nowSec}`)
      })
      $('.badges').append(badgeEl)
    }
  })
}

showBadgesToAdd()

function updateScores() {
  $.get(`${$SCRIPT_ROOT}/badge/_scores_later_than?child_id=${$CHILD_ID}&timestamp=${lastSundaySec}`, (scores) => {

    var weeklyScores = []
    for (var i = 0; i < 7; i++) {
      weeklyScores.push([])
    }
    for (let score of scores) {
      weeklyScores[new Date(score.timestamp).getDay()].push(score)
    }
    for (var i = 0; i < 7; i++) {
      var box = $('.score-box').eq(i)
      box.empty()
      for (let score of weeklyScores[i]) {
        var scoreEl = createBadgeEl(score.image_url)
        box.append(scoreEl)
      }
    }
  })
}


var scoreCount
function checkChildScoreCount() {
  $.get(`${$SCRIPT_ROOT}/family/_child_score_count?child_id=${$CHILD_ID}`, (currentCount)=>{
    if (scoreCount === currentCount) return
    scoreCount = currentCount
    updateScores()
  })
}

setInterval(() => {
  checkChildScoreCount()
}, 500);