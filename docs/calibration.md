# Guided Gesture Calibration Guide

Hand sizes vary across users. The adaptive calibration system normalizes gesture distance based on your specific physical hand dimensions.

## Step-by-Step Calibration Workflow

1. Open the dashboard at `http://127.0.0.1:3000`.
2. Click **Calibrate Bounds** in the Gesture Status panel.
3. **Step 1 (MIN Distance):**
   - Bring your Thumb tip and Index finger tip close together (pinched position).
   - Click **Record Minimum Distance**.
4. **Step 2 (MAX Distance):**
   - Spread your Thumb tip and Index finger tip wide apart.
   - Click **Record Maximum Distance**.
5. **Step 3 (Save):**
   - Click **Save Calibration Parameters**.

Your custom gesture limits are saved locally in SQLite and applied immediately.
