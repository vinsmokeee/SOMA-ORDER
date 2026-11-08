# Putting SOMA on its own website (works offline)

The app in `docs/` is the same SOMA app, saving orders to a free Google Firebase database.
Firebase keeps a copy on each phone, so SOMA opens and saves orders without internet and
syncs both phones when a connection comes back. No Claude account is needed.

## 1. Create the Firebase project (owner, once, about 10 minutes)

Do this in Chrome. A laptop is easier, but a phone works.

1. Go to https://console.firebase.google.com and sign in with a Google account.
2. **Create a project** → name it `soma-orders` → turn **Google Analytics off** → **Create project**.
3. **Build → Firestore Database → Create database**
   - Location: **asia-south1 (Mumbai)**, the closest to Bhutan.
   - Choose **Start in production mode** → **Create**.
4. **Build → Authentication → Get started → Email/Password** → turn on the first switch → **Save**.
5. **Authentication → Users → Add user**
   - Your email and a password → **Add user**.
   - Your girlfriend's email and a password → **Add user**.
   - Copy each person's **User UID** (the long code in the list).
6. **Project settings (gear icon) → General → Your apps → Web (`</>`)**
   - App nickname `SOMA` → leave "Firebase Hosting" unticked → **Register app**.
   - Copy the `firebaseConfig = { ... }` block.

Send Claude the `firebaseConfig` block and the two **User UIDs**.
**Never send passwords.** The config and UIDs are not secret.

## 2. Lock the database to your two accounts

Claude fills the UIDs into `firestore.rules`. Then:

**Firestore Database → Rules** → replace everything with the contents of `firestore.rules` → **Publish**.

Without this step nobody can read or save orders, because production mode blocks everything.

## 3. Publish the website (GitHub Pages)

1. On GitHub, open the repository → **Settings → Pages**.
2. **Source: Deploy from a branch** → branch `main` (after merging) → folder **/docs** → **Save**.
3. After a minute the site is at `https://vinsmokeee.github.io/SOMA-ORDER/`.
4. Back in Firebase: **Authentication → Settings → Authorized domains → Add domain** → `vinsmokeee.github.io`.

GitHub Pages is free for public repositories. The code and Firebase settings in this repository
contain no customer data; orders live only in Firebase, behind the rules above.

## 4. Install on each phone

1. Open the site in **Chrome** (Android) or **Safari** (iPhone) and sign in once.
2. Android: **⋮ → Add to Home screen → Install**. iPhone: **Share → Add to Home Screen**.

The SOMA logo becomes the app icon, and the app opens full screen like a normal app.
The first sign-in needs internet. After that SOMA opens offline.

## Updating the app

Edit `index.html`, run `python3 build.py`, commit `docs/`. Phones pick up the new version the
next time SOMA is opened online.
