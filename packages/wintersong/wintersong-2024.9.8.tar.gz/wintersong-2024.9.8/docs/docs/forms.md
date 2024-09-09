# Forms

<form>
  <label>First name</label>
  <input
    name="first_name"
    placeholder="First name"
    autocomplete="given-name" />
  <label>Email</label>
  <input
    type="email"
    name="email"
    placeholder="Email"
    autocomplete="email" />
  <small>This is some help text</small>
  <label>Number</label>
  <input type="number" name="number" placeholder="Number" min="0" max="100" step="1" />
  <label>Disabled</label>
  <input disabled value="meep" />
  <label>Readonly</label>
  <div role="group">
    <input readonly value="meep" />
    <button type="button"><winter-icon>content_copy</winter-icon></button>
  </div>
  <label>Validation</label>
  <input value="meep" aria-invalid="true" />
  <small>Looks bad!</small>
  <input value="meep" aria-invalid="false" />
  <small>Looks good!</small>
  <label>Range</label>
  <input type="range" value="50" min="0" max="100" />
  <label>
    <input type="checkbox" name="checkbox" checked />
    Checkbox
  </label>
  <label>
    <input type="checkbox" name="checkbox" disabled />
    Checkbox (disabled)
  </label>
  <label>
    <input type="radio" name="language" checked />
    English
  </label>
  <label>
    <input type="radio" name="language" />
    French
  </label>
  <label>Select</label>
  <select name="favorite-cuisine" aria-label="Select your favorite cuisine..." required>
    <option selected disabled value="">
      Select your favorite cuisine...
    </option>
    <option>Italian</option>
    <option>Japanese</option>
    <option>Indian</option>
    <option>Thai</option>
    <option>French</option>
  </select>
  <label>Textarea</label>
  <textarea>Oh god how did this get here I am not good with computer.</textarea>
  <input
    type="submit"
    value="Subscribe"
  />
</form>
