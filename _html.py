# from allennlp sever_simple.py
import re
from string import Template
from typing import List

_PAGE_TEMPLATE = Template(
"""
<html>
    <head>
        <title>
            $title
        </title>
        <style>
            $css
        </style>
    </head>
    <body>
        <div class="pane-container">
            <div class="pane model">
                <div class="pane__left model__input">
                    <div class="model__content">
                        <h2><span>$title</span></h2>
                        <div class="model__content">
                            <div id="input-document-id" style="display: none;"></div>
                            <div id="input-answer-label" style="display: none;"></div>
                            <div class="form__field form__field--btn">
                                <button type="button" class="btn btn--icon-disclosure" style="margin-left: 10px;" onclick="get_original()">
                                    Revert
                                </button>
                                <button type="button" class="btn btn--icon-disclosure" style="margin-left: 10px;" onclick="ablate_example('drop_function_words')">
                                    Drop stopwords!
                                </button>
                                <button type="button" class="btn btn--icon-disclosure" style="margin-left: 10px;" onclick="ablate_example('shuffle_document')">
                                    Shuffle Document!
                                </button>
                                <button type="button" class="btn btn--icon-disclosure" style="margin-left: 10px;" onclick="ablate_example('shuffle_question')">
                                    Shuffle Question!
                                </button>
                                <button type="button" class="btn btn--icon-disclosure" style="margin-left: 10px;" onclick="get_example()">
                                    Get Example
                                </button>
                                <button type="button" class="btn btn--icon-disclosure" onclick="predict()">
                                    Predict
                                </button>
                            </div>
                            $inputs
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    <script>
function predict() {
    for (var i = 0; i < 4; i++) {
        if (!document.getElementById("input-option" + (i + 1).toString() + "-spec")) break;
        document.getElementById("input-option" + (i + 1).toString() + "-spec").innerHTML = "";
    }
    var quotedFieldList = $qfl;
    var data = {};
    quotedFieldList.forEach(function(fieldName) {
        data[fieldName] = document.getElementById("input-" + fieldName).value;
    })
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/predict');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status == 200) {
            // If you want a more impressive visualization than just
            // outputting the raw JSON, change this part of the code.
            var response_data = JSON.parse(xhr.responseText);
            var htmlResults = "<pre>" + JSON.stringify(response_data, null, 2) + "</pre>";
            var best_option = response_data["result"];
            for (var i = 0; i < 4; i++) {
                if (!document.getElementById("input-option" + (i + 1).toString() + "-spec")) break;
                var percentage = Math.round(response_data["result"][i]*100);
                document.getElementById("input-option" + (i + 1).toString() + "-spec").innerHTML = drawPercentBar(100, percentage.toString(), '#2ECC71');
                if (i == response_data["prediction"]) {
                    document.getElementById("input-option" + (i + 1).toString() + "-spec").innerHTML += '<span style=\"margin-left: 5px;\">&#11088;</span>';
                }
            }
        }
    };
    xhr.send(JSON.stringify(data));
}

function drawPercentBar(width, percent, color, background) {
    var barhtml = "";
    var pixels = width * (percent / 100);
    barhtml += '<span style=\"display: inline-block; text-align: center; width: 70px; \">(' + percent + '%)</span>';

    barhtml += '<span style=\"display: inline-block; vertical-align: text-top; width: 100px; border: 1px solid black;\">';

    barhtml += '<div style=\"height: 1.125em; width: ' + pixels + 'px; background-color: '
        + color + ';\"></div>';

    barhtml += "</span>";

    return barhtml;
}

function get_example() {
    for (var i = 0; i < 4; i++) {
        if (!document.getElementById("input-option" + (i + 1).toString() + "-spec")) break;
        document.getElementById("input-option" + (i + 1).toString() + "-spec").innerHTML = "";
    }
    var quotedFieldList = $qfl;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get-example');
    xhr.onload = function() {
        if (xhr.status == 200) {
            // If you want a more impressive visualization than just
            // outputting the raw JSON, change this part of the code.
            var response_data = JSON.parse(xhr.responseText);
            quotedFieldList.forEach(function(fieldName) {
                var element = document.getElementById("input-" + fieldName);
                element.value = response_data[fieldName];
                var event = new Event('input', {
                    bubbles: true,
                    cancelable: true,
                });
                element.dispatchEvent(event);
            });
            document.getElementById("input-document-id").innerHTML = response_data["example_id"];
            document.getElementById("input-document-spec").innerHTML = '<span style=\"margin-left: 10px;\">(ID: ' + response_data["example_id"] + ')</span>';
            document.getElementById("input-answer-label").innerHTML = response_data["label"];
            document.getElementById("input-question-spec").innerHTML = '<span style=\"margin-left: 10px;\">(Answer: option' + (parseInt(response_data["label"]) + 1).toString() + ')</span>';
        }
    };
    xhr.send();
}

function get_original() {
    for (var i = 0; i < 4; i++) {
        if (!document.getElementById("input-option" + (i + 1).toString() + "-spec")) break;
        document.getElementById("input-option" + (i + 1).toString() + "-spec").innerHTML = "";
    }
    var quotedFieldList = $qfl;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/revert');
    xhr.onload = function() {
        if (xhr.status == 200) {
            // If you want a more impressive visualization than just
            // outputting the raw JSON, change this part of the code.
            var response_data = JSON.parse(xhr.responseText);
            quotedFieldList.forEach(function(fieldName) {
                var element = document.getElementById("input-" + fieldName);
                element.value = response_data[fieldName];
                var event = new Event('input', {
                    bubbles: true,
                    cancelable: true,
                });
                element.dispatchEvent(event);
            });
            document.getElementById("input-document-id").innerHTML = response_data["example_id"];
            document.getElementById("input-document-spec").innerHTML = '<span style=\"margin-left: 10px;\">(ID: ' + response_data["example_id"] + ')</span>';
            document.getElementById("input-answer-label").innerHTML = response_data["label"];
            document.getElementById("input-question-spec").innerHTML = '<span style=\"margin-left: 10px;\">(Answer: option' + (parseInt(response_data["label"]) + 1).toString() + ')</span>';
        }
    };
    xhr.send();
}

function ablate_example(ablation_type) {
    var quotedFieldList = $qfl;
    var data = {};
    quotedFieldList.forEach(function(fieldName) {
        data[fieldName] = document.getElementById("input-" + fieldName).value;
    })
    data["example_id"] = document.getElementById("input-document-id").value;
    data["label"] = document.getElementById("input-answer-label").value;
    data["specification"] = ablation_type;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/ablate');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status == 200) {
            // If you want a more impressive visualization than just
            // outputting the raw JSON, change this part of the code.
            var response_data = JSON.parse(xhr.responseText);
            quotedFieldList.forEach(function(fieldName) {
                var element = document.getElementById("input-" + fieldName);
                element.value = response_data[fieldName];
                var event = new Event('input', {
                    bubbles: true,
                    cancelable: true,
                });
                element.dispatchEvent(event);
            });
            if (response_data["example_id"]) {
                document.getElementById("input-document-id").innerHTML = response_data["example_id"];
                document.getElementById("input-document-spec").innerHTML = '<span style=\"margin-left: 10px;\">(ID: ' + response_data["example_id"] + ')</span>';
            }
            if (response_data["specification"]) {
                document.getElementById("input-document-spec").innerHTML += '<span style=\"margin-left: 10px;\">(' + response_data["specification"] + ')</span>';
            }
            if (response_data["label"]) {
                document.getElementById("input-answer-label").innerHTML = response_data["label"];
                document.getElementById("input-question-spec").innerHTML = '<span style=\"margin-left: 10px;\">(Answer: option' + (parseInt(response_data["label"]) + 1).toString() + ')</span>';
            }
        }
    };
    xhr.send(JSON.stringify(data));
}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

    </script>
</html>
"""
)


_SINGLE_INPUT_TEMPLATE = Template(
    """
        <div class="form__field">
            <label for="input-$field_name">$field_name<span id="input-$field_name-spec"></span></label>
            <input type="text" id="input-$field_name" type="text" required value placeholder="input goes here">
        </div>
    """
)

_SINGLE_TEXTAREA_TEMPLATE = Template(
    """
        <div class="form__field">
            <label for="input-$field_name">$field_name<span id="input-$field_name-spec"></span></label>
            <textarea oninput="auto_grow(this)" type="text" id="input-$field_name" type="text" required value placeholder="input goes here"></textarea>
        </div>
    """
)

_SINGLE_LABEL_TEMPLATE = """
        <div class="form__field">
            <label for="input-options">options</label>
        </div>
"""

_SINGLE_OPTION_TEMPLATE = Template(
    """
        <div class="form__field">
            <label style="float: left; line-height: 2.75em;" for="input-option$option_num">$option_num.</label>
            <div style="display: block; overflow: hidden;">
                <textarea rows="1" oninput="auto_grow(this)" style="float: left; width: 70%; margin-left: 10px; height: 2.75em;" type="text" id="input-option$option_num" required="" value="" placeholder="input goes here"></textarea>
                <span id="input-option$option_num-spec" style="line-height: 2.75em;"></span>
            </div>
        </div>
    """
)


_CSS = """
body,
html {
  min-width: 48em;
  background: #f9fafc;
  font-size: 16px
}
* {
  font-family: sans-serif;
  color: #232323
}
section {
  background: #fff
}
code,
code span,
pre,
.output {
  font-family: 'Roboto Mono', monospace!important
}
code {
  background: #f6f8fa
}
li,
p,
td,
th {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 1.125em;
  line-height: 1.5em;
  margin: 1.2em 0
}
pre {
  margin: 2em 0
}
h1,
h2 {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-weight: 300
}
h2 {
  font-size: 2em;
  color: rgba(35, 35, 35, .75)
}
img {
  max-width: 100%
}
hr {
  display: block;
  border: none;
  height: .375em;
  background: #f6f8fa
}
blockquote,
hr {
  margin: 2.4em 0
}
.btn {
  text-decoration: none;
  cursor: pointer;
  font-size: 1em;
  margin: 0;
  -moz-appearance: none;
  -webkit-appearance: none;
  border: none;
  color: #fff!important;
  display: block;
  background: #2085bc;
  padding: .6375em 1.625em;
  -webkit-transition: background-color .2s ease, opacity .2s ease;
  transition: background-color .2s ease, opacity .2s ease;
  margin-left: 10px;
}
.btn.btn--blue {
  background: #2085bc
}
.btn:focus,
.btn:hover {
  background: #40affd;
  outline: 0
}
.btn:focus {
  box-shadow: 0 0 1.25em rgba(50, 50, 150, .05)
}
.btn:active {
  opacity: .66;
  background: #2085bc;
  -webkit-transition-duration: 0s;
  transition-duration: 0s
}
.btn:disabled,
.btn:disabled:active,
.btn:disabled:hover {
  cursor: default;
  background: #d0dae3
}
form {
  display: block
}
.form__field {
  -webkit-transition: margin .2s ease;
  transition: margin .2s ease
}
.form__field+.form__field {
  margin-top: 1.5em
}
.form__field label {
  display: block;
  font-weight: 600;
  font-size: 1.125em
}
.form__field label+* {
  margin-top: 1em
}
.form__field input[type=text],
.form__field textarea {
  -moz-appearance: none;
  -webkit-appearance: none;
  width: 100%;
  font-size: 1em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  padding: .8125em 1.125em;
  color: #232323;
  border: .125em solid #d4dce2;
  display: block;
  box-sizing: border-box;
  -webkit-transition: background-color .2s ease, color .2s ease, border-color .2s ease, opacity .2s ease;
  transition: background-color .2s ease, color .2s ease, border-color .2s ease, opacity .2s ease
}
.form__field input[type=text]::-webkit-input-placeholder,
.form__field textarea::-webkit-input-placeholder {
  color: #b4b4b4
}
.form__field input[type=text]:-moz-placeholder,
.form__field textarea:-moz-placeholder {
  color: #b4b4b4
}
.form__field input[type=text]::-moz-placeholder,
.form__field textarea::-moz-placeholder {
  color: #b4b4b4
}
.form__field input[type=text]:-ms-input-placeholder,
.form__field textarea:-ms-input-placeholder {
  color: #b4b4b4
}
.form__field input[type=text]:focus,
.form__field textarea:focus {
  outline: 0;
  border-color: #63a7d4;
  box-shadow: 0 0 1.25em rgba(50, 50, 150, .05)
}
.form__field textarea {
  /* resize: vertical; */
  /* min-height: 8.25em */
}
.form__field .btn {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-touch-callout: none
}
.form__field--btn {
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: row;
  -ms-flex-direction: row;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  flex-direction: row;
  -webkit-justify-content: flex-end;
  -ms-justify-content: flex-end;
  -webkit-box-pack: end;
  -ms-flex-pack: end;
  justify-content: flex-end
}
@media screen and (max-height:760px) {
  .form__instructions {
    margin: 1.875em 0 1.125em
  }
  .form__field:not(.form__field--btn)+.form__field:not(.form__field--btn) {
    margin-top: 1.25em
  }
}
body,
html {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Source Sans Pro', sans-serif
}
h1 {
  font-weight: 300
}
.model__output {
  background: #fff
}
.model__output.model__output--empty {
  background: 0 0
}
.placeholder {
  width: 100%;
  height: 100%;
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: center;
  -ms-flex-align: center;
  -webkit-box-align: center;
  align-items: center;
  -webkit-justify-content: center;
  -ms-justify-content: center;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-touch-callout: none;
  cursor: default
}
.placeholder .placeholder__content {
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
  -ms-flex-direction: column;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  flex-direction: column;
  -webkit-align-items: center;
  -ms-flex-align: center;
  -webkit-box-align: center;
  align-items: center;
  text-align: center
}
.placeholder svg {
  display: block
}
.placeholder svg.placeholder__empty,
.placeholder svg.placeholder__error {
  width: 6em;
  height: 3.625em;
  fill: #e1e5ea;
  margin-bottom: 2em
}
.placeholder svg.placeholder__error {
  width: 4.4375em;
  height: 4em
}
.placeholder p {
  font-size: 1em;
  margin: 0;
  padding: 0;
  color: #9aa8b2
}
.placeholder svg.placeholder__working {
  width: 3.4375em;
  height: 3.4375em;
  -webkit-animation: working 1s infinite linear;
  animation: working 1s infinite linear
}
@-webkit-keyframes working {
  0% {
    -webkit-transform: rotate(0deg)
  }
  100% {
    -webkit-transform: rotate(360deg)
  }
}
@keyframes working {
  0% {
    -webkit-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    transform: rotate(0deg)
  }
  100% {
    -webkit-transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    transform: rotate(360deg)
  }
}
.model__content {
  padding: 1.875em 2.5em;
  margin: auto;
  -webkit-transition: padding .2s ease;
  transition: padding .2s ease
}
.model__content:not(.model__content--srl-output) {
  max-width: 61.25em
}
.model__content h2 {
  margin: 0;
  padding: 0;
  font-size: 1em
}
.model__content h2 span {
  font-size: 2em;
  color: rgba(35, 35, 35, .75)
}
.model__content h2 .tooltip,
.model__content h2 span {
  vertical-align: top
}
.model__content h2 span+.tooltip {
  margin-left: .4375em
}
.model__content>h2:first-child {
  margin: -.25em 0 0 -.03125em
}
.model__content__summary {
  font-size: 1em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  padding: 1.25em;
  background: #f6f8fa
}
@media screen and (min-height:800px) {
  .model__content {
    /* padding-top: 4.6vh; */
    padding-bottom: 4.6vh
  }
}
.pane-container {
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
  -ms-flex-direction: column;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  flex-direction: column;
  height: 100%
}
.pane {
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: row;
  -ms-flex-direction: row;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  flex-direction: row;
  position: relative;
  -webkit-box-flex: 2;
  -webkit-flex: 2;
  -ms-flex: 2;
  flex: 2;
  height: auto;
  min-height: 100%;
  min-height: 34.375em
}
.pane__left,
.pane__right {
  width: 100%;
  height: 100%;
  -webkit-align-self: stretch;
  -ms-flex-item-align: stretch;
  align-self: stretch;
  min-width: 24em;
  min-height: 34.375em
}
.pane__left {
  height: auto;
  min-height: 100%
}
.pane__right {
  width: 100%;
  overflow: auto;
  height: auto;
  min-height: 100%
}
.pane__right .model__content.model__content--srl-output {
  display: inline-block;
  margin: auto
}
.pane__thumb {
  height: auto;
  min-height: 100%;
  margin-left: -.625em;
  position: absolute;
  width: 1.25em
}
.pane__thumb:after {
  display: block;
  position: absolute;
  height: 100%;
  top: 0;
  content: "";
  width: .25em;
  background: #e1e5ea;
  left: .5em
}
"""


def _html(title: str, field_names: List[str]) -> str:
    """
    Returns bare bones HTML for serving up an input form with the
    specified fields that can render predictions from the configured model.
    """
    inputs = ""
    for field_name in field_names:
        if field_name == "document":
            inputs += _SINGLE_TEXTAREA_TEMPLATE.substitute(field_name=field_name)
        elif field_name == "option_header":
            inputs += _SINGLE_LABEL_TEMPLATE
        elif field_name.startswith("option"):
            option_num = re.findall(r'\d+', field_name)[0]
            inputs += _SINGLE_OPTION_TEMPLATE.substitute(option_num=option_num)
        else:
            inputs += _SINGLE_INPUT_TEMPLATE.substitute(field_name=field_name)

    quoted_field_names = (f"'{field_name}'" for field_name in field_names if field_name != 'option_header')
    quoted_field_list = f"[{','.join(quoted_field_names)}]"

    return _PAGE_TEMPLATE.substitute(title=title, css=_CSS, inputs=inputs, qfl=quoted_field_list)

