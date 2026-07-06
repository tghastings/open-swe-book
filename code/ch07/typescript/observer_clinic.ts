// §7.2.2 Observers and Subscribers — a subject that notifies without knowing
// its observers' concrete types (clinic scheduler: waiting-room display).
type Observer = (appointment: Appointment) => void;

class Appointment {
  status: string;
  private observers: Observer[] = [];

  constructor(status: string = "booked") {
    this.status = status;
  }

  subscribe(callback: Observer): void {
    this.observers.push(callback);
  }

  setStatus(newStatus: string): void {
    this.status = newStatus;
    for (const notify of this.observers) notify(this);  // any callback will do
  }
}

const waitingRoomDisplay: Observer = (appointment) =>
  console.log(`display: appointment is now ${appointment.status}`);

const appt = new Appointment();
appt.subscribe(waitingRoomDisplay);
appt.setStatus("arrived");               // prints: display: appointment is now arrived

import assert from "node:assert";
assert.strictEqual(appt.status, "arrived");
