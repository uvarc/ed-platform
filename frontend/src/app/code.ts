import {Links} from './links';
import {Workshop} from './workshop';
import {Track} from "./track";

export class Code {
  id: String;
  description: String;
  prereq = false;
  status: String;
  links = new Links();
  workshops = Array<Workshop>();
  workshop_ids = Array<Number>();
  track_count = 0;

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.workshops = Array<Workshop>();
    if ('workshops' in values) {
      for (const w of values['workshops']) {
          this.workshops.push(new Workshop(w));
      }
    }
  }

  attended() { return this.status === 'ATTENDED'; }
  awaiting_review() { return this.status === 'AWAITING_REVIEW'; }
  registered() { return this.status === 'REGISTERED'; }

  color() {
    if (this.attended()) { return 'primary'; }
    if (this.awaiting_review()) { return 'primary'; }
    return 'primary';
  }

  icon() {
    if (this.attended()) { return 'checked'; }
    if (this.awaiting_review()) { return 'checked'; }
    if (this.registered()) { return 'circle-full'; }
    return 'circle-open';
  }

  progress_icon() {
    if (this.prereq) { return 'connector'; }
    return 'connector-blank';
  }


}
