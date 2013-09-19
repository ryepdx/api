$(document).ready(function () {
	$response = $("#response");
	$submit = $("input[type=submit]");
	$seed = $("input[name=seed]");
	
	sjcl.random.startCollectors();
	setInterval(function () {
		$seed.val(sjcl.random.randomWords(1)[0]);
	}, 1000);

	$("input[name=usd]").keyup(function () {
		var $this = $(this);
		var usd = parseInt($this.val());
		
		if ($this.val() == "") {
			$response.text('');
			$submit.hide();
			$submit.attr("disabled", true);
		} else if (isNaN(usd)) {
			$response.text('"That doesn\'t appear to be a number, old chum."');
			$submit.hide();
			$submit.attr("disabled", true);
		} else if (usd > 1000) {
			$response.text('"I can\'t do more than $1000 per person per day, old sport."');
			$submit.hide();
			$submit.attr("disabled", true);
		} else {
			var satoshis = 100000000;
			var btc = (new Big((new Big(usd)).div(SELL_PRICE).times(satoshis).toPrecision(8))).div(satoshis);
			$response.text('"That will get you ' + btc + ' BTC."');
			$submit.attr("disabled", false);
			$submit.show();
		}
	});
});
