let meta = #{
    name: "chinese-novelist-factory",
    description: "Factory-mode: complete one chinese-novelist-skill chapter or short-story transaction, then verify with scripts",
    when_to_use: "批量写, 自动写完整本, 快写下一章, factory chapter",
    phases: [
        #{ title: "Transaction", detail: "one atomic factory transaction" },
    ],
};

let report_schema = #{
    "type": "object",
    "required": ["status", "passed", "paths", "summary"],
    "properties": #{
        "status": #{ "type": "string" },
        "book": #{ "type": "string" },
        "chapter": #{ "type": "integer" },
        "passed": #{ "type": "boolean" },
        "paths": #{ "type": "array", "items": #{ "type": "string" } },
        "summary": #{ "type": "string" },
        "recovery": #{ "type": "string" },
    },
};

phase("Transaction");

let extra = "";
if args != () {
    if args.novel != () {
        extra += " Novel directory: ";
        extra += args.novel;
        extra += ".";
    }
    if args.chapter != () {
        extra += " Target chapter: ";
        extra += args.chapter.to_string();
        extra += ".";
    }
}

let prompt = "";
prompt += "You are executing chinese-novelist-skill in factory mode. ";
prompt += "Read SKILL.md and references/batch-production.md with read_file before writing. ";
prompt += "Do not load every file in references/. ";
prompt += extra;
prompt += " Complete exactly one atomic transaction: one long-form chapter or one complete short story. ";
prompt += "Write recoverable artifacts to disk. manuscript/zh/ is the only source of truth for Chinese chapter text. ";
prompt += "Run python3 scripts/check_chapter_transaction.py with --factory for a novel chapter, or python3 scripts/check_short_story.py for a short story. ";
prompt += "If the check fails, fix once and rerun. If it fails twice, stop and report recovery. ";
prompt += "Do not paste chapter or 6000+ character short-story bodies into your final answer. ";
prompt += "Return status as one of: advanced, complete, failed, blocked.";

let r = agent(prompt, #{
    label: "factory-tx",
    capability_mode: "all",
    output_schema: report_schema,
});

if r == () || r.success == false || r.output == () {
    await_user("verification", "Factory agent did not return a usable report. Inspect files, then resume to retry one transaction.");
    r = agent(prompt, #{
        label: "factory-tx-retry",
        capability_mode: "all",
        output_schema: report_schema,
    });
}

if r == () || r.success == false || r.output == () {
    complete(#{
        status: "failed",
        passed: false,
        paths: [],
        summary: "Factory agent did not return a usable report after retry.",
        recovery: "Inspect novels/ or short-stories/, then rerun /workflow chinese-novelist-factory.",
    });
}

if r.output.passed == false {
    await_user("verification", "Transaction did not pass. Fix artifacts, then resume to retry one transaction.");
    r = agent(prompt, #{
        label: "factory-tx-fix",
        capability_mode: "all",
        output_schema: report_schema,
    });
}

if r == () || r.success == false || r.output == () {
    complete(#{
        status: "failed",
        passed: false,
        paths: [],
        summary: "Factory retry did not return a usable report.",
        recovery: "Inspect novels/ or short-stories/, then rerun /workflow chinese-novelist-factory.",
    });
}

complete(r.output);
