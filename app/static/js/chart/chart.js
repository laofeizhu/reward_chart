const dayEntry = $(`
<tr>
<td width="5%"><h4 class="chart-date"></h4></td>
<td><div class="level is-mobile"><div class="score-box level-left is-multiline "></div></div></td>
</tr>
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

// Updates add star date on the modal
function updateAddStarDate() {
  var d = new Date(addScoreMs)
  $('#score-date').text('Select to add a star to ' + '(' + (d.getMonth() + 1) + '/' + d.getDate() + ') ' + DAYS[d.getDay()])
}

var scoreBalance = 0
function updateScoreBalance() {
  $.get(`${$SCRIPT_ROOT}/family/_child_score_balance?child_id=${$CHILD_ID}`, (score)=>{
    scoreBalance = score
    getAndShowReward()
    $('#score-balance').text('Score Balance: ' + scoreBalance)
  })
}

updateScoreBalance()

function showAddStarModal() {
  $('#add-star').addClass("is-active")
}

function closeAddStarModal() {
  $('#add-star').removeClass("is-active")
}

updateAddStarDate()

var getClickCb = (i) => {
  return () => {
    addScoreMs = nowMs + (i - day) * oneDay
    updateAddStarDate()
    showAddStarModal()
  }
}

for (var i = 0; i < 7; ++i) {
  var row = dayEntry.clone()
  $('#chart-body').append(row)
  $('.chart-date').eq(i).click(getClickCb(i))
}

function updateTime() {
  let oldlastSundayMs = lastSundayMs
  let oldDay = day
  var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var lastSunday = new Date(today.setDate(today.getDate()-today.getDay()));
  day = now.getDay()
  lastSundayMs = lastSunday.getTime()
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
  $('#confirm-delete-star').removeClass("is-active")
})

$('#cancel-add').click(() => {
  closeAddStarModal()
})

$('#confirm-removal').click(() => {
  $.post(`${$SCRIPT_ROOT}/badge/_delete_score?score_id=${scoreToRemove.id}&child_id=${$CHILD_ID}`, ()=>{
    updateScores()
    $('#confirm-delete-star').removeClass("is-active")
  })
})

function createBadgeEl(image_url) {
  return $(`<div class="level-item is-narrow"><p class="image is-64x64">
            <img src=${$SCRIPT_ROOT}/${image_url}>
          </p></div>`)
}

var scoreToRemove = null
function createScoreEl(score) {
  var el = createBadgeEl(score.image_url)
  el.click(() => {
    scoreToRemove = score
    $("#confirm-delete-star").addClass("is-active")
  })
  return el
}

function showBadgesToAdd() {
  $.get($SCRIPT_ROOT + '/badge/_get_badges_for_child/' + $CHILD_ID, function(badges) {
    for (let badge of badges) {
      var badgeEl = createBadgeEl(badge.image_url)
      badgeEl.click(() => {
        // add to earlier days if earlier days are selected
        $.post(`${$SCRIPT_ROOT}/badge/_score?child_id=${$CHILD_ID}&badge_id=${badge.id}&timestamp=${addScoreMs}`, ()=>{
           updateScores()
           closeAddStarModal()
         })
      })
      $('.badges').append(badgeEl)
    }
  })
}

showBadgesToAdd()

function updateScores() {
  updateScoreBalance()
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

var currentReward
var rewardImageEl = $('#reward-image')
var rewardProgressTextEl = $('#progress-text')
var rewardProgressBarEl = $('#progress-bar')
function getAndShowReward() {
  $.get(`${$SCRIPT_ROOT}/family/_current_reward?child_id=${$CHILD_ID}`, (reward) => {
    currentReward = reward
    console.log(reward)
    rewardImageEl.attr('src', `${$SCRIPT_ROOT}/${currentReward["image_url"]}`)
    rewardProgressTextEl.text(`${scoreBalance}/${reward["score"]}`)
    rewardProgressBarEl.attr('value', `${scoreBalance}`, 'max', `${reward["score"]}`)
  })
}
