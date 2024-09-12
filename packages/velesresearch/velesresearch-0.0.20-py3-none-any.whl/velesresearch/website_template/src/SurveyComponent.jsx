import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/survey.i18n";
import "survey-core/defaultV2.min.css";
import { json } from "./survey.js";
import * as SurveyCore from "survey-core";
import { nouislider } from "surveyjs-widgets";
import "nouislider/distribute/nouislider.css";
import * as config from "./config.js";
import CSRFToken from "./csrf.js";

nouislider(SurveyCore);

function MakeID(length) {
  let result = "";
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}

function groupNumber(max) {
  return Math.floor(Math.random() * max + 1);
}

function SurveyComponent() {
  const survey = new Model(json);
  const date_started = new Date();

  document.documentElement.lang = survey.locale;

  survey.setVariable("group", groupNumber(config.numberOfGroups));
  survey.setVariable("date_started", date_started.toISOString());

  survey.onComplete.add((sender) => {
    const date_completed = new Date();
    survey.setVariable("date_completed", date_completed.toISOString());

    const variables = {};
    for (const variable in survey.getVariableNames()) {
      variables[variable] = survey.getVariable(variable);
    }

    const URLparams = Object.fromEntries(new URLSearchParams(window.location.search));

    const result = Object.assign(
      {
        id: MakeID(8)
      },
      sender.data,
      URLparams,
      variables
    );

    // send data to Django backend
    fetch(window.location.pathname + "submit/", {
      method: "POST",
      headers: Object.assign(
        {
          "Content-Type": "application/json",
        },
        CSRFToken()
      ),
      body: JSON.stringify(result),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
      });
  });
  return <Survey model={survey} />;
}

export default SurveyComponent;
