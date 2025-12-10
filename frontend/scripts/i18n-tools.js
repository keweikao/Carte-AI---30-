#!/usr/bin/env node

/**
 * i18n Management Tools
 *
 * Provides automated tools for managing internationalization files:
 * - Check consistency across all language files
 * - Initialize new language files with TODO placeholders
 * - Sync structure across all languages
 */

const fs = require('fs');
const path = require('path');

const MESSAGES_DIR = path.join(__dirname, '../messages');
const REFERENCE_LOCALE = 'zh-TW'; // Reference locale for structure

// ANSI color codes for pretty output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

/**
 * Get all locale files in the messages directory
 */
function getLocaleFiles() {
  const files = fs.readdirSync(MESSAGES_DIR);
  return files
    .filter(file => file.endsWith('.json'))
    .map(file => ({
      locale: file.replace('.json', ''),
      path: path.join(MESSAGES_DIR, file)
    }));
}

/**
 * Load a JSON file
 */
function loadJSON(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`${colors.red}Error loading ${filePath}:${colors.reset}`, error.message);
    return null;
  }
}

/**
 * Save a JSON file with pretty formatting
 */
function saveJSON(filePath, data) {
  try {
    const content = JSON.stringify(data, null, 4);
    fs.writeFileSync(filePath, content + '\n', 'utf-8');
    return true;
  } catch (error) {
    console.error(`${colors.red}Error saving ${filePath}:${colors.reset}`, error.message);
    return false;
  }
}

/**
 * Get all keys in a nested object as paths (e.g., "HomePage.title")
 */
function getKeyPaths(obj, prefix = '') {
  const paths = [];

  for (const [key, value] of Object.entries(obj)) {
    const currentPath = prefix ? `${prefix}.${key}` : key;

    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      paths.push(...getKeyPaths(value, currentPath));
    } else {
      paths.push(currentPath);
    }
  }

  return paths;
}

/**
 * Get value from nested object using path (e.g., "HomePage.title")
 */
function getValueByPath(obj, path) {
  return path.split('.').reduce((current, key) => current?.[key], obj);
}

/**
 * Set value in nested object using path (e.g., "HomePage.title")
 */
function setValueByPath(obj, path, value) {
  const keys = path.split('.');
  const lastKey = keys.pop();
  const target = keys.reduce((current, key) => {
    if (!current[key]) current[key] = {};
    return current[key];
  }, obj);
  target[lastKey] = value;
}

/**
 * Check consistency across all locale files
 */
function checkConsistency() {
  console.log(`${colors.cyan}🔍 Checking i18n consistency...${colors.reset}\n`);

  const localeFiles = getLocaleFiles();
  const referenceFile = localeFiles.find(f => f.locale === REFERENCE_LOCALE);

  if (!referenceFile) {
    console.error(`${colors.red}❌ Reference locale ${REFERENCE_LOCALE}.json not found!${colors.reset}`);
    process.exit(1);
  }

  const referenceData = loadJSON(referenceFile.path);
  if (!referenceData) {
    console.error(`${colors.red}❌ Failed to load reference file${colors.reset}`);
    process.exit(1);
  }

  const referenceKeys = getKeyPaths(referenceData);
  console.log(`${colors.blue}📋 Reference (${REFERENCE_LOCALE}): ${referenceKeys.length} keys${colors.reset}\n`);

  let hasErrors = false;

  // Check each locale file
  for (const localeFile of localeFiles) {
    if (localeFile.locale === REFERENCE_LOCALE) continue;

    console.log(`${colors.magenta}Checking ${localeFile.locale}...${colors.reset}`);

    const data = loadJSON(localeFile.path);
    if (!data) {
      hasErrors = true;
      continue;
    }

    const keys = getKeyPaths(data);
    const missingKeys = referenceKeys.filter(key => !keys.includes(key));
    const extraKeys = keys.filter(key => !referenceKeys.includes(key));

    // Check for empty or TODO values
    const todoKeys = keys.filter(key => {
      const value = getValueByPath(data, key);
      return typeof value === 'string' && (value.trim() === '' || value.includes('TODO') || value.includes('待翻譯'));
    });

    if (missingKeys.length === 0 && extraKeys.length === 0 && todoKeys.length === 0) {
      console.log(`  ${colors.green}✓ Perfect! All ${keys.length} keys match${colors.reset}`);
    } else {
      hasErrors = true;

      if (missingKeys.length > 0) {
        console.log(`  ${colors.red}✗ Missing ${missingKeys.length} keys:${colors.reset}`);
        missingKeys.slice(0, 5).forEach(key => {
          console.log(`    - ${key}`);
        });
        if (missingKeys.length > 5) {
          console.log(`    ... and ${missingKeys.length - 5} more`);
        }
      }

      if (extraKeys.length > 0) {
        console.log(`  ${colors.yellow}⚠ Extra ${extraKeys.length} keys (not in reference):${colors.reset}`);
        extraKeys.slice(0, 5).forEach(key => {
          console.log(`    - ${key}`);
        });
        if (extraKeys.length > 5) {
          console.log(`    ... and ${extraKeys.length - 5} more`);
        }
      }

      if (todoKeys.length > 0) {
        console.log(`  ${colors.yellow}⚠ ${todoKeys.length} keys need translation (TODO/empty):${colors.reset}`);
        todoKeys.slice(0, 5).forEach(key => {
          console.log(`    - ${key}`);
        });
        if (todoKeys.length > 5) {
          console.log(`    ... and ${todoKeys.length - 5} more`);
        }
      }
    }

    console.log();
  }

  if (hasErrors) {
    console.log(`${colors.red}❌ Consistency check failed. Please fix the issues above.${colors.reset}`);
    console.log(`${colors.cyan}💡 Run 'npm run i18n:sync' to automatically fix structure issues.${colors.reset}`);
    process.exit(1);
  } else {
    console.log(`${colors.green}✅ All locale files are consistent!${colors.reset}`);
  }
}

/**
 * Initialize a new locale file with TODO placeholders
 */
function initLocale(newLocale) {
  console.log(`${colors.cyan}🌐 Initializing new locale: ${newLocale}${colors.reset}\n`);

  const referenceFile = getLocaleFiles().find(f => f.locale === REFERENCE_LOCALE);
  if (!referenceFile) {
    console.error(`${colors.red}❌ Reference locale ${REFERENCE_LOCALE}.json not found!${colors.reset}`);
    process.exit(1);
  }

  const newFilePath = path.join(MESSAGES_DIR, `${newLocale}.json`);
  if (fs.existsSync(newFilePath)) {
    console.error(`${colors.red}❌ Locale file ${newLocale}.json already exists!${colors.reset}`);
    process.exit(1);
  }

  const referenceData = loadJSON(referenceFile.path);
  if (!referenceData) {
    console.error(`${colors.red}❌ Failed to load reference file${colors.reset}`);
    process.exit(1);
  }

  // Create a deep copy with TODO placeholders
  function createTodoStructure(obj) {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        result[key] = createTodoStructure(value);
      } else {
        result[key] = `TODO: Translate from ${REFERENCE_LOCALE}`;
      }
    }
    return result;
  }

  const newData = createTodoStructure(referenceData);

  if (saveJSON(newFilePath, newData)) {
    const keyCount = getKeyPaths(newData).length;
    console.log(`${colors.green}✅ Created ${newLocale}.json with ${keyCount} keys (all marked TODO)${colors.reset}`);
    console.log(`${colors.cyan}💡 Next step: Translate the TODO values in ${newFilePath}${colors.reset}`);
  } else {
    console.error(`${colors.red}❌ Failed to create new locale file${colors.reset}`);
    process.exit(1);
  }
}

/**
 * Sync structure across all locale files
 */
function syncStructure() {
  console.log(`${colors.cyan}🔄 Syncing locale file structures...${colors.reset}\n`);

  const localeFiles = getLocaleFiles();
  const referenceFile = localeFiles.find(f => f.locale === REFERENCE_LOCALE);

  if (!referenceFile) {
    console.error(`${colors.red}❌ Reference locale ${REFERENCE_LOCALE}.json not found!${colors.reset}`);
    process.exit(1);
  }

  const referenceData = loadJSON(referenceFile.path);
  if (!referenceData) {
    console.error(`${colors.red}❌ Failed to load reference file${colors.reset}`);
    process.exit(1);
  }

  const referenceKeys = getKeyPaths(referenceData);

  for (const localeFile of localeFiles) {
    if (localeFile.locale === REFERENCE_LOCALE) continue;

    console.log(`${colors.magenta}Syncing ${localeFile.locale}...${colors.reset}`);

    const data = loadJSON(localeFile.path);
    if (!data) continue;

    const keys = getKeyPaths(data);
    const missingKeys = referenceKeys.filter(key => !keys.includes(key));
    const extraKeys = keys.filter(key => !referenceKeys.includes(key));

    let modified = false;

    // Add missing keys with TODO
    if (missingKeys.length > 0) {
      console.log(`  ${colors.yellow}Adding ${missingKeys.length} missing keys...${colors.reset}`);
      missingKeys.forEach(key => {
        setValueByPath(data, key, `TODO: Translate from ${REFERENCE_LOCALE}`);
      });
      modified = true;
    }

    // Remove extra keys
    if (extraKeys.length > 0) {
      console.log(`  ${colors.yellow}Removing ${extraKeys.length} extra keys...${colors.reset}`);

      // Rebuild object without extra keys
      const cleanedData = {};
      referenceKeys.forEach(key => {
        const value = getValueByPath(data, key);
        if (value !== undefined) {
          setValueByPath(cleanedData, key, value);
        }
      });
      Object.assign(data, cleanedData);

      // Clear the original data and rebuild
      for (const key of Object.keys(data)) {
        delete data[key];
      }
      for (const [key, value] of Object.entries(cleanedData)) {
        data[key] = value;
      }

      modified = true;
    }

    if (modified) {
      if (saveJSON(localeFile.path, data)) {
        console.log(`  ${colors.green}✓ Updated successfully${colors.reset}`);
      } else {
        console.log(`  ${colors.red}✗ Failed to save${colors.reset}`);
      }
    } else {
      console.log(`  ${colors.green}✓ Already in sync${colors.reset}`);
    }

    console.log();
  }

  console.log(`${colors.green}✅ Structure sync complete!${colors.reset}`);
  console.log(`${colors.cyan}💡 Run 'npm run i18n:check' to verify consistency${colors.reset}`);
}

/**
 * List all TODO items across all locales
 */
function listTodos() {
  console.log(`${colors.cyan}📝 Finding all TODO translations...${colors.reset}\n`);

  const localeFiles = getLocaleFiles();
  let totalTodos = 0;

  for (const localeFile of localeFiles) {
    const data = loadJSON(localeFile.path);
    if (!data) continue;

    const keys = getKeyPaths(data);
    const todoKeys = keys.filter(key => {
      const value = getValueByPath(data, key);
      return typeof value === 'string' && (value.includes('TODO') || value.includes('待翻譯') || value.trim() === '');
    });

    if (todoKeys.length > 0) {
      console.log(`${colors.magenta}${localeFile.locale}: ${todoKeys.length} TODOs${colors.reset}`);
      todoKeys.forEach(key => {
        const value = getValueByPath(data, key);
        console.log(`  - ${key}: "${value}"`);
      });
      console.log();
      totalTodos += todoKeys.length;
    }
  }

  if (totalTodos === 0) {
    console.log(`${colors.green}✅ No TODO translations found!${colors.reset}`);
  } else {
    console.log(`${colors.yellow}Total: ${totalTodos} translations need work${colors.reset}`);
  }
}

/**
 * Main CLI
 */
function main() {
  const command = process.argv[2];
  const arg = process.argv[3];

  switch (command) {
    case 'check':
      checkConsistency();
      break;

    case 'init':
      if (!arg) {
        console.error(`${colors.red}❌ Please specify a locale code (e.g., npm run i18n:init ja)${colors.reset}`);
        process.exit(1);
      }
      initLocale(arg);
      break;

    case 'sync':
      syncStructure();
      break;

    case 'todos':
      listTodos();
      break;

    default:
      console.log(`${colors.cyan}i18n Management Tools${colors.reset}\n`);
      console.log('Available commands:');
      console.log(`  ${colors.green}check${colors.reset}        - Check consistency across all locale files`);
      console.log(`  ${colors.green}init <locale>${colors.reset} - Initialize a new locale file with TODO placeholders`);
      console.log(`  ${colors.green}sync${colors.reset}         - Sync structure across all locale files`);
      console.log(`  ${colors.green}todos${colors.reset}        - List all TODO translations`);
      console.log('\nExamples:');
      console.log('  npm run i18n:check');
      console.log('  npm run i18n:init ja');
      console.log('  npm run i18n:sync');
      console.log('  npm run i18n:todos');
      process.exit(0);
  }
}

main();
