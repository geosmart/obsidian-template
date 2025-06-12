'use strict';

var obsidian = require('obsidian');
var path = require('path');

function _interopNamespace(e) {
    if (e && e.__esModule) return e;
    var n = Object.create(null);
    if (e) {
        Object.keys(e).forEach(function (k) {
            if (k !== 'default') {
                var d = Object.getOwnPropertyDescriptor(e, k);
                Object.defineProperty(n, k, d.get ? d : {
                    enumerable: true,
                    get: function () {
                        return e[k];
                    }
                });
            }
        });
    }
    n['default'] = e;
    return Object.freeze(n);
}

var path__namespace = /*#__PURE__*/_interopNamespace(path);

/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

function __awaiter(thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
}

function convertPathToHtmlFragment(path, pathContainsFileName, includeIcons) {
    const fragment = new DocumentFragment();
    const pathParts = getPathParts(path, pathContainsFileName);
    pathParts.forEach((part) => {
        fragment.appendChild(getNodeForPathPart(part, includeIcons));
    });
    return fragment;
}
function getNodeForPathPart(part, includeIcon) {
    const fragment = new DocumentFragment();
    switch (part.type) {
        case 0 /* FOLDER */:
            if (includeIcon) {
                fragment.appendText(`📁 `);
            }
            fragment.appendText(part.name);
            break;
        case 1 /* FILE */:
            if (includeIcon) {
                fragment.appendText(`📄 `);
            }
            fragment.appendText(part.name);
            break;
        case 2 /* SEPARATOR */:
            fragment.appendText(` » `);
            break;
    }
    return fragment;
}
function getPathParts(path, lastPartIsFile) {
    if (path === '/') {
        return [{ type: 0 /* FOLDER */, name: 'Vault Root' }];
    }
    else {
        const parts = path.split('/');
        const pathParts = [];
        parts.forEach((partName) => {
            pathParts.push({ type: 0 /* FOLDER */, name: partName });
            pathParts.push({ type: 2 /* SEPARATOR */ });
        });
        // Remove last separator
        pathParts.pop();
        if (lastPartIsFile) {
            pathParts[pathParts.length - 1].type = 1 /* FILE */;
        }
        return pathParts;
    }
}

const DEFAULT_SETTINGS = {
    showFileName: false,
    showIcons: true,
    copyAbsolutePath: false,
};
class FilePathPlugin extends obsidian.Plugin {
    constructor(app, pluginManifest) {
        super(app, pluginManifest);
    }
    onload() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.loadSettings();
            const statusBarItem = this.addStatusBarItem();
            const showFile = (file) => {
                if (!file)
                    return;
                const pathToDisplay = this.settings.showFileName
                    ? file.path
                    : file.parent.path;
                const fragment = convertPathToHtmlFragment(pathToDisplay, this.settings.showFileName, this.settings.showIcons);
                statusBarItem.innerHTML = '';
                statusBarItem.appendChild(fragment);
            };
            const copyPathToClipboard = () => {
                const activeFile = this.app.workspace.getActiveFile();
                // The last open file is closed, no currently open files
                if (!activeFile) {
                    return;
                }
                const relativePath = this.settings.showFileName
                    ? activeFile.path
                    : activeFile.parent.path;
                const absolutePath = path__namespace.join(this.app.vault.adapter.basePath, relativePath);
                const textToCopy = this.settings.copyAbsolutePath
                    ? absolutePath
                    : relativePath;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    new obsidian.Notice("Path copied to clipboard");
                });
            };
            this.registerEvent(this.app.workspace.on('file-open', showFile));
            this.registerEvent(this.app.vault.on('rename', file => {
                if (file instanceof obsidian.TFile && file === this.app.workspace.getActiveFile())
                    showFile(file);
            }));
            this.addSettingTab(new SettingsTab(this.app, this));
            statusBarItem.classList.add('mod-clickable');
            statusBarItem.addEventListener('click', copyPathToClipboard);
            this.addCommand({
                id: 'copy-file-path',
                name: 'Copy path',
                callback: copyPathToClipboard
            });
        });
    }
    loadSettings() {
        return __awaiter(this, void 0, void 0, function* () {
            this.settings = Object.assign({}, DEFAULT_SETTINGS, yield this.loadData());
        });
    }
    saveSettings() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.saveData(this.settings);
        });
    }
}
class SettingsTab extends obsidian.PluginSettingTab {
    constructor(app, plugin) {
        super(app, plugin);
        this.app = app;
        this.plugin = plugin;
    }
    display() {
        const { containerEl } = this;
        containerEl.empty();
        containerEl.createEl('h2', { text: 'Settings' });
        new obsidian.Setting(containerEl)
            .setName('Show file name')
            .setDesc('Include name of open file in the path')
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.showFileName)
            .onChange((value) => __awaiter(this, void 0, void 0, function* () {
            this.plugin.settings.showFileName = value;
            yield this.plugin.saveSettings();
        })));
        new obsidian.Setting(containerEl)
            .setName('Show icons')
            .setDesc('Show folder and file icons')
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.showIcons)
            .onChange((value) => __awaiter(this, void 0, void 0, function* () {
            this.plugin.settings.showIcons = value;
            yield this.plugin.saveSettings();
        })));
        new obsidian.Setting(containerEl)
            .setName('Copy absolute path')
            .setDesc('Copy absolute path on clicking status bar')
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.copyAbsolutePath)
            .onChange((value) => __awaiter(this, void 0, void 0, function* () {
            this.plugin.settings.copyAbsolutePath = value;
            yield this.plugin.saveSettings();
        })));
    }
}

module.exports = FilePathPlugin;


/* nosourcemap */