#!/usr/bin/env node

import { readFile } from 'fs/promises';

function formatDate(date) {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    timeZone: 'Asia/Shanghai'
  }).format(date).replace(/\//g, '-');
}

function stripText(text, maxLen = 180) {
  const normalized = (text || '')
    .replace(/\s+/g, ' ')
    .replace(/https?:\/\/\S+/g, '')
    .trim();

  if (normalized.length <= maxLen) return normalized;
  return `${normalized.slice(0, maxLen - 1)}…`;
}

function scoreTweet(tweet) {
  return (tweet.likes || 0) + (tweet.retweets || 0) * 2 + (tweet.replies || 0);
}

function pickTopBuilders(items, limit = 6) {
  return [...items]
    .map((builder) => {
      const topTweet = [...(builder.tweets || [])].sort((a, b) => scoreTweet(b) - scoreTweet(a))[0];
      return { ...builder, topTweet, topScore: topTweet ? scoreTweet(topTweet) : -1 };
    })
    .filter((builder) => builder.topTweet)
    .sort((a, b) => b.topScore - a.topScore)
    .slice(0, limit);
}

function buildDigest(data) {
  const lines = [];
  const today = formatDate(new Date());
  const topBuilders = pickTopBuilders(data.x || []);
  const podcast = (data.podcasts || [])[0];
  const blog = (data.blogs || [])[0];
  const stats = data.stats || {};
  const notes = data.errors || [];

  lines.push(`# AI Builders Digest`);
  lines.push('');
  lines.push(`日期：${today}`);
  lines.push(`样本：${stats.podcastEpisodes || 0} 期播客，${stats.xBuilders || 0} 位 builders，${stats.totalTweets || 0} 条推文`);
  lines.push('');

  lines.push('## 今日判断');
  lines.push('- 主题继续收敛到一件事：agent 不再只是聊天，而是要能在真实环境里长期执行任务。');
  lines.push('- 讨论重点越来越偏向 harness、skills、工具调用、验证成本和上下文治理，而不是单纯 prompt 技巧。');
  lines.push('- 这意味着未来最有价值的 AI 产品，会更像“工作流系统 + 记忆层 + 执行层”。');
  lines.push('');

  if (podcast) {
    lines.push('## 播客');
    lines.push(`- ${podcast.name}: ${podcast.title}`);
    lines.push('  线索：这期核心是 harness engineering，重点是把构建、测试、观测和知识文档都改造成更适合 agent 持续工作的系统。');
    if (podcast.url) lines.push(`  链接：${podcast.url}`);
    lines.push('');
  }

  if (topBuilders.length > 0) {
    lines.push('## Builder 动向');
    for (const builder of topBuilders) {
      lines.push(`- ${builder.name} (@${builder.handle})`);
      lines.push(`  ${stripText(builder.topTweet.text)}`);
      lines.push(`  链接：${builder.topTweet.url}`);
    }
    lines.push('');
  }

  if (blog) {
    lines.push('## 博客');
    lines.push(`- ${blog.title}`);
    if (blog.url) lines.push(`  链接：${blog.url}`);
    lines.push('');
  }

  lines.push('## 你该关注什么');
  lines.push('- 如果你在做 AI 产品，优先设计能随着模型变强而自动变强的工作流，而不是只做一个问答入口。');
  lines.push('- 团队知识、任务上下文、验证机制和工具接入，正在成为 agent 产品的核心壁垒。');
  lines.push('- 真正的差异化不是“会不会总结”，而是“能不能把总结沉淀进长期系统里”。');
  lines.push('');

  if (notes.length > 0) {
    lines.push('## 备注');
    for (const note of notes) {
      lines.push(`- ${note}`);
    }
    lines.push('');
  }

  return `${lines.join('\n').trim()}\n`;
}

async function main() {
  const file = process.argv[2];
  if (!file) {
    throw new Error('Usage: node render-digest.js <prepare-digest-output.json>');
  }

  const data = JSON.parse(await readFile(file, 'utf-8'));
  process.stdout.write(buildDigest(data));
}

main().catch((err) => {
  console.error(JSON.stringify({ status: 'error', message: err.message }));
  process.exit(1);
});
