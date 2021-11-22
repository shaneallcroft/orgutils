<!DOCTYPE html>
<html>
<head>
<script>// credit to this repo https://github.com/maqboolkhan/Collapsible-list/blob/master/ul.js
window.onload = function  () {
	var li_ul = document.querySelectorAll(".col_ul li  ul");
    for (var i = 0; i < li_ul.length; i++) {
        li_ul[i].style.display = "none"
    };
    var exp_li = document.querySelectorAll(".col_ul li > span");
    for (var i = 0; i < exp_li.length; i++) {
        exp_li[i].style.cursor = "pointer";
        exp_li[i].onclick = showul;
    };
    function showul () {
        nextul = this.nextElementSibling;
        if(nextul.style.display == "block")
            nextul.style.display = "none";
        else
            nextul.style.display = "block";
    }
}</script>
<meta name="orghtml" content="width=device-width, initial-scale=1">
</head>
<body>
<style>
body {
font-family: "Roberto", sans-serif;
font-size: 17px;
    background-color: #fdfdfd;
}
.shadow {
    box-shadow: 0 4px 2px -2px rgba(0, 0, 0, 0.1);
}
.btn-danger {
    color: #fff;
    background-color: #f00000;
    border-color: #dc281e;    
}
.masthead {
    background: #3398E1;
    height: auto;
    padding-bottom: 15px;
    box-shadow: 0 16px 48px #E3E7EB;
    padding-top: 10px;
}
</style>
<ul class="col_ul"><li> <span>html_translate</span>
<ul><li> <span>html header</span>
<ul><li><!DOCTYPE html>
<html>
<head>
<script></li>
</ul>
 </li>
<li> <span>org behavior javascript</span>
<ul><li>// credit to this repo https://github.com/maqboolkhan/Collapsible-list/blob/master/ul.js
window.onload = function  () {
	var li_ul = document.querySelectorAll(".col_ul li  ul");
    for (var i = 0; i < li_ul.length; i++) {
        li_ul[i].style.display = "none"
    };
    var exp_li = document.querySelectorAll(".col_ul li > span");
    for (var i = 0; i < exp_li.length; i++) {
        exp_li[i].style.cursor = "pointer";
        exp_li[i].onclick = showul;
    };
    function showul () {
        nextul = this.nextElementSibling;
        if(nextul.style.display == "block")
            nextul.style.display = "none";
        else
            nextul.style.display = "block";
    }
}</li>
</ul>
 </li>
<li> <span>style</span>
<ul><li></script>
<meta name="orghtml" content="width=device-width, initial-scale=1">
</head>
<body>
<style>
body {
font-family: "Roberto", sans-serif;
font-size: 17px;
    background-color: #fdfdfd;
}
.shadow {
    box-shadow: 0 4px 2px -2px rgba(0, 0, 0, 0.1);
}
.btn-danger {
    color: #fff;
    background-color: #f00000;
    border-color: #dc281e;    
}
.masthead {
    background: #3398E1;
    height: auto;
    padding-bottom: 15px;
    box-shadow: 0 16px 48px #E3E7EB;
    padding-top: 10px;
}
</style>
<ul class="col_ul"></li>
</ul>
 </li>
<li> <span>recursive html ---u-></span>
<ul><li>    if not node_to_translate.isLeaf:
        for child in node_to_translate.contentOrdered:
            ret_str += '<li> <span>' + str(child.key) + '</span>
<ul>'
            ret_str += ---R->(child)
            ret_str += '</ul>
 </li>
'
    else:
      # Base case reached
        ret_str += '<li>' + str(node_to_translate.getValue()) + '</li>
'</li>
</ul>
 </li>
<li> <span>body code cap</span>
<ul><li></body>
</li>
</ul>
 </li>
</ul>
 </li>
</body>
0
0

