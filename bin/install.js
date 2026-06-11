#!/usr/bin/env node
/**
 * pm-skills — install/uninstall the PM skill collection into ~/.claude/skills
 *
 * Usage:
 *   pm-skills install [--target <dir>] [--only <name,name>] [--dry-run]
 *   pm-skills uninstall [--target <dir>] [--only <name,name>]
 *   pm-skills list [--target <dir>]
 */
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

const PKG_ROOT = path.resolve(__dirname, "..");

function findSkills() {
  return fs
    .readdirSync(PKG_ROOT, { withFileTypes: true })
    .filter(
      (e) =>
        e.isDirectory() &&
        fs.existsSync(path.join(PKG_ROOT, e.name, "SKILL.md"))
    )
    .map((e) => e.name)
    .sort();
}

function parseArgs(argv) {
  const args = { command: "install", target: null, only: null, dryRun: false };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--target") args.target = argv[++i];
    else if (a === "--only") args.only = argv[++i];
    else if (a === "--dry-run") args.dryRun = true;
    else if (a === "--help" || a === "-h") args.command = "help";
    else rest.push(a);
  }
  if (rest.length > 0) args.command = rest[0];
  return args;
}

function targetDir(args) {
  if (args.target) return path.resolve(args.target);
  return path.join(os.homedir(), ".claude", "skills");
}

function selectSkills(args) {
  const all = findSkills();
  if (!args.only) return all;
  const wanted = args.only.split(",").map((s) => s.trim()).filter(Boolean);
  const unknown = wanted.filter((w) => !all.includes(w));
  if (unknown.length > 0) {
    console.error(`未知 skill: ${unknown.join(", ")}`);
    console.error(`可用: ${all.join(", ")}`);
    process.exit(1);
  }
  return wanted;
}

function copySkill(name, dest, dryRun) {
  const src = path.join(PKG_ROOT, name);
  const dst = path.join(dest, name);
  const existed = fs.existsSync(dst);
  if (!dryRun) {
    fs.rmSync(dst, { recursive: true, force: true });
    fs.cpSync(src, dst, {
      recursive: true,
      filter: (p) => path.basename(p) !== ".DS_Store",
    });
  }
  return existed;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const dest = targetDir(args);

  if (args.command === "help") {
    console.log(
      [
        "pm-skills <command> [options]",
        "",
        "Commands:",
        "  install     复制全部 skill 到 ~/.claude/skills（默认，已存在则更新）",
        "  uninstall   从 ~/.claude/skills 移除本合集的 skill",
        "  list        列出包内 skill 及安装状态",
        "",
        "Options:",
        "  --target <dir>      指定目标目录（默认 ~/.claude/skills）",
        "  --only <a,b>        只处理指定 skill",
        "  --dry-run           只显示将执行的操作",
      ].join("\n")
    );
    return;
  }

  const skills = selectSkills(args);

  if (args.command === "list") {
    for (const name of skills) {
      const installed = fs.existsSync(path.join(dest, name, "SKILL.md"));
      console.log(`${installed ? "[已安装]" : "[未安装]"} ${name}`);
    }
    console.log(`\n目标目录: ${dest}`);
    return;
  }

  if (args.command === "uninstall") {
    for (const name of skills) {
      const dst = path.join(dest, name);
      if (!fs.existsSync(dst)) {
        console.log(`跳过（不存在）: ${name}`);
        continue;
      }
      if (!args.dryRun) fs.rmSync(dst, { recursive: true, force: true });
      console.log(`已移除: ${dst}`);
    }
    return;
  }

  if (args.command === "install") {
    if (!args.dryRun) fs.mkdirSync(dest, { recursive: true });
    for (const name of skills) {
      const existed = copySkill(name, dest, args.dryRun);
      console.log(
        `${args.dryRun ? "[dry-run] " : ""}${existed ? "已更新" : "已安装"}: ${name} -> ${path.join(dest, name)}`
      );
    }
    console.log(
      `\n完成。共 ${skills.length} 个 skill。重启 Claude Code 会话后生效。`
    );
    return;
  }

  console.error(`未知命令: ${args.command}（用 --help 查看用法）`);
  process.exit(1);
}

main();
