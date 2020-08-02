
function createRewardEl(reward) {
  return $(`
      <article class="media" id="reward-id-${reward.id}">
        <figure class="media-left">
          <p class="image is-64x64">
            <img src=${$SCRIPT_ROOT}/${reward.image_url}>
          </p>
        </figure>
        <div class="media-content">
          <div class="content">
            <p>
              <strong>${reward.name}</strong>
            </p>
          </div>
        </div>
      </article>
  `)
}

var deleteEl = $(`
        <div class="media-right">
          <button class="delete" id="delete-reward"></button>
        </div>
 `)

var rewardToRemove
var getDeleteRewardCallback = (rewardId) => {
  return () => {
    rewardToRemove = rewardId
    $('#confirm-delete-reward').addClass("is-active")
  }
}
function listRewards() {
  var rewardListEl = $("#reward-list")

  $.get(`${$SCRIPT_ROOT}/reward/_get_rewards`, (rewards) => {
    console.log(rewards)
    for (var reward of rewards) {
      var rewardEl = createRewardEl(reward)
      if (reward.id.indexOf('default') == -1) {
        rewardEl.append(deleteEl.clone())
        rewardEl.find('#delete-reward').click(getDeleteRewardCallback(reward.id))
      }
      rewardListEl.append(rewardEl)
    }
  })
}

listRewards()

$('#cancel-removal').click(() => {
  $('#confirm-delete-reward').removeClass("is-active")
})

$('#confirm-removal').click(() => {
  var rewardEl = $(`#reward-id-${rewardToRemove}`)
  $.post(`${$SCRIPT_ROOT}/reward/_delete_reward?reward_id=${rewardToRemove}`, () => {
    rewardEl.remove()
    $('#confirm-delete-reward').removeClass("is-active")
  })
})