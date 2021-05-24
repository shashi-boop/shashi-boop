console.log("Background script loaded")

var contextMenuItem = {

	"id": "Clickbait",
	"title": "Check if Clickbait or Not",
	"contexts": ["link"]	
};

chrome.contextMenus.create(contextMenuItem);

chrome.contextMenus.onClicked.addListener(function(clickData){
	if(clickData.menuItemId == "Clickbait"){
		console.log("Context Selection taken place")
		console.log("Link Url: "+clickData.linkUrl)
		console.log("Page Url: "+clickData.pageUrl)
		

		var request_pagelink = new XMLHttpRequest();
		request_pagelink.onreadystatechange = function(){
			if(request_pagelink.readyState==4){
				if(request_pagelink.status=400)
				{
					var data=JSON.parse(request_pagelink.responseText);
					window.clickbait=data.clickbaitiness.toString();
					console.log("XMLHttp Request Perfect");
					console.log(clickbait)

					window.percent_data= {
							cb_percentage : clickbait
						}
							console.log("data added")
				}
			}
		};

		var request_urllink = new XMLHttpRequest();
		request_urllink.onreadystatechange = function(){
			if(request_urllink.readyState==4){
				if(request_urllink.status=400)
				{
					var data=JSON.parse(request_urllink.responseText);
					window.clickbait=data.clickbaitiness.toString();
					console.log("XMLHttp Request Perfect");
					console.log(clickbait)
					var alert_text = ""
					alert_text = clickData.linkUrl
					alert_text += "\nClickbait Percentage: " + clickbait
					alert_text += "\nStatus: "
					if(clickbait>50)
					{
						alert_text += "Is a clickbait"
					}
					else{
						alert_text += "Is not a clickbait"
					}
					alert(alert_text)
				}
			}
		};

		window.msg= {
			link_url : clickData.linkUrl,
			page_url : clickData.pageUrl
		}

		request_pagelink.open("GET", "https://clickbait-detector.herokuapp.com/detect?headline=" + clickData.pageUrl, true);
		request_pagelink.send();

		request_urllink.open("GET", "https://clickbait-detector.herokuapp.com/detect?headline=" + clickData.linkUrl, true);
		request_urllink.send();


	}
});