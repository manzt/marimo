/* Copyright 2023 Marimo. All rights reserved. */
import { test, expect } from "@playwright/test";
import { getAppUrl } from "../playwright.config";

test("page renders edit feature in edit mode", async ({ page }) => {
  const appUrl = getAppUrl("title.py");
  await page.goto(appUrl);

  // Has elements with class name 'controls'
  expect(await page.locator("#save-button").count()).toBeGreaterThan(0);

  // Can see output
  await expect(page.locator("h1").getByText("Hello Marimo!")).toBeVisible();
});

test("can toggle to read mode", async ({ page }) => {
  const appUrl = getAppUrl("title.py");
  await page.goto(appUrl);

  // Can see output and code
  await expect(page.locator("h1").getByText("Hello Marimo!")).toBeVisible();
  await expect(page.getByText("# Hello Marimo!")).toBeVisible();

  // Toggle preview-button
  await page.locator("#preview-button").click();

  // Can see output
  await expect(page.locator("h1").getByText("Hello Marimo!")).toBeVisible();
  // No code
  await expect(page.getByText("# Hello Marimo!")).not.toBeVisible();

  // Toggle preview-button again
  await page.locator("#preview-button").click();

  // Can see output and code
  await expect(page.locator("h1").getByText("Hello Marimo!")).toBeVisible();
  await expect(page.getByText("# Hello Marimo!")).toBeVisible();
});

test("page renders read only view in read mode", async ({ page }) => {
  const appUrl = getAppUrl("components.py");
  await page.goto(appUrl);

  // Filename is not visible
  await expect(page.getByText("components.py").last()).not.toBeVisible();
  // Has elements with class name 'controls'
  expect(await page.locator("#save-button").count()).toBe(0);

  // Can see output
  await expect(page.locator("h1").getByText("UI Elements")).toBeVisible();
});
