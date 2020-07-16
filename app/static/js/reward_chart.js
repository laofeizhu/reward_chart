const dayEntry = $(`
<article class="media">
  <h4 class="media-left chart-date"></h4>
  <div class="media-content">
    <div class="content score-box columns is-multiline is-gapless is-vcentered"></div>
  </div>
</article>
`)


const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
var oneDay = 24 * 3600 * 1000
var oneHour = 3600 * 1000
var oneMin = 60 * 1000
var oneSec = 1000

var now = new Date()
var nowMs = now.getTime()
var lastSundayMs = null
var day = null
var addScoreMs = nowMs

function showAddStarDate() {
  var d = new Date(addScoreMs)
  $('#score-date').text('Adding star to ' + '(' + (d.getMonth() + 1) + '/' + d.getDate() + ') ' + DAYS[d.getDay()])
}

showAddStarDate()

var getClickCb = (i) => {
  return () => {
    addScoreMs = nowMs + (i - day) * oneDay
    showAddStarDate()
  }
}

for (var i = 0; i < 7; ++i) {
  var row = dayEntry.clone()
  row.children('.chart-date').click(getClickCb(i))
  $('#chart-body').append(row)
}

function updateTime() {
  let oldlastSundayMs = lastSundayMs
  let oldDay = day
  day = now.getDay()
  lastSundayMs = nowMs - oneDay * now.getDay() - oneHour * now.getHours() - oneMin * now.getMinutes() - oneSec * now.getSeconds()
  if (oldlastSundayMs != lastSundayMs) {
    for (var i = 0; i < 7; ++i) {
      var d = new Date(lastSundayMs + i * oneDay)
      $('.chart-date').eq(i).text('(' + (d.getMonth() + 1) + '/' + d.getDate() + ') ' + DAYS[i])
    }
  }
  if (day != oldDay) {
    for (var i = 0; i < 7; ++i) {
      $('.chart-date').eq(i).removeClass('has-background-primary')
    }
    $('.chart-date').eq(now.getDay()).addClass('has-background-primary')
  }
  if (oldlastSundayMs !== lastSundayMs) {
    updateScores()
  }
}

// do a time update immediately
updateTime()

setInterval(() => {
  now = new Date()
  nowMs = now.getTime()
  updateTime()
}, 5000)


$('#cancel-removal').click(() => {
  $('.modal').removeClass("is-active")
})

$('#modal-close').click(() => {
  $('.modal').removeClass("is-active")
})

$('#confirm-removal').click(() => {
  $.post(`${$SCRIPT_ROOT}/badge/_delete_score?score_id=${scoreToRemove.id}&child_id=${$CHILD_ID}`, ()=>{
    updateScores()
    $('.modal').removeClass("is-active")
  })
})

function createBadgeEl(image_url) {
  return $(`<div class="column is-narrow"><figure class="image is-64x64">
  <img src=${$SCRIPT_ROOT}/file/${image_url}>
</figure></div>`)
}

var scoreToRemove = null
function createScoreEl(score) {
  var el = createBadgeEl(score.image_url)
  el.click(() => {
    scoreToRemove = score
    $(".modal").addClass("is-active")
  })
  return el
}

function showBadgesToAdd() {
  $.get($SCRIPT_ROOT + '/badge/_get_badges_for_child/' + $CHILD_ID, function(badges) {
    for (let badge of badges) {
      var badgeEl = createBadgeEl(badge.image_url)
      badgeEl.click(() => {
        // add to earlier days if earlier days are selected
        $.post(`${$SCRIPT_ROOT}/badge/_score?child_id=${$CHILD_ID}&badge_id=${badge.id}&timestamp=${addScoreMs}`, ()=>{ updateScores() })
      })
      $('.badges').append(badgeEl)
    }
  })
}

showBadgesToAdd()

function updateScores() {
  $.get(`${$SCRIPT_ROOT}/badge/_scores_later_than?child_id=${$CHILD_ID}&timestamp=${lastSundayMs}`, (scores) => {

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
        var scoreEl = createScoreEl(score)
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
}, 5000);