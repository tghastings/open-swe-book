import assert from "node:assert";

// Domain and clinic app under test (stubbed so the steps run on their own):
interface Patient { interpreter: boolean; }
interface Visit { banners: string[]; }
interface ClinicWorld { patient: Patient; visit: Visit; }

function checkIn(opts: { interpreter: boolean }): Patient {
  return { interpreter: opts.interpreter };
}
function openVisit(patient: Patient): Visit {
  return { banners: patient.interpreter ? ["interpreter needed"] : [] };
}

// A typed stand-in for @cucumber/cucumber's step registry:
type Step = (this: ClinicWorld) => void;
const steps = new Map<string, Step>();
const define = (name: string, fn: Step): Map<string, Step> => steps.set(name, fn);
const Given = define, When = define, Then = define;

Given("a checked-in patient flagged for an interpreter", function (this: ClinicWorld) {
  this.patient = checkIn({ interpreter: true });
});
Given("a checked-in patient with no interpreter flag", function (this: ClinicWorld) {
  this.patient = checkIn({ interpreter: false });
});
When("the clinician opens the visit", function (this: ClinicWorld) {
  this.visit = openVisit(this.patient);
});
Then('an "interpreter needed" banner is shown', function (this: ClinicWorld) {
  assert.ok(this.visit.banners.includes("interpreter needed"));
});
Then("no interpreter banner is shown", function (this: ClinicWorld) {
  assert.equal(this.visit.banners.length, 0);
});

// Drive both scenarios the way a BDD runner would, then assert they pass:
function runScenario(lines: string[]): void {
  const world = {} as ClinicWorld;
  for (const line of lines) steps.get(line)!.call(world);
}
runScenario([
  "a checked-in patient flagged for an interpreter",
  "the clinician opens the visit",
  'an "interpreter needed" banner is shown',
]);
runScenario([
  "a checked-in patient with no interpreter flag",
  "the clinician opens the visit",
  "no interpreter banner is shown",
]);
console.log("both scenarios pass");
