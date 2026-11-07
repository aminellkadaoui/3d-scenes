# 3D Scenes

نظام معرفي لـClaude Code يساعدك تبني مشاهد Blender سينمائية (VSL، إعلانات، ريلز) بسرعة وبجودة عالية على EEVEE. المعرفة كلها مأخوذة من مشاريع حقيقية: المشاكل اللي صارت، وأسبابها، والحلول بالأرقام.

A Claude Code plugin that turns real Blender production experience into reusable knowledge: EEVEE quality recipes, light linking ("track matte" lighting), turntable spin + object match cut, camera crane, materials, a symptom → fix table, ready bpy scripts, and a retro skill that grows the knowledge after every project.

## وش فيه
| الجزء | الوظيفة |
|---|---|
| `3d-scenes` (Skill) | المخرج: مسار العمل، والـFeedback loop، ويوجّه للملف المناسب |
| `references/` | 12 ملف معرفة متخصص (الإضاءة، الخامات، الحركة، النويز، الرندر، المشاكل…) |
| `scripts/` | سكربتات bpy جاهزة (Turntable، Match cut، Light linking، جودة EEVEE، كمرة كرين…) |
| `case-studies/` | مشاريع كاملة بكل قراراتها وأرقامها |
| `lessons/LESSONS.md` | قواعد قصيرة تكبر مع كل مشروع |
| `3d-scenes-retro` (Skill) | بعد كل مشروع: يحوّل اللي تعلمناه لقواعد ويحدّث النظام |

## المتطلبات
- Claude Code.
- Blender 5.x مع إضافة **Blender MCP** (عشان Claude يتحكم في Blender المفتوح).
- اختياري: ffmpeg و numpy لتحليل الريفرنسات.

## التثبيت
من مجلد محلي:
```bash
claude plugin marketplace add "/path/to/3D-Scenes"
```
```bash
claude plugin install 3d-scenes@3d-scenes
```
أو من داخل Claude Code: `/plugin marketplace add <المسار أو رابط GitHub>` ثم `/plugin install 3d-scenes@3d-scenes`.

للمشاركة: ارفع المجلد كامل على GitHub (ريبو خاص أو عام)، وأصحابك يضيفونه بـ`/plugin marketplace add <user>/<repo>`.

## الاستخدام
اكتب طلبك عادي: «سوي لي مشهد لابتوب يدور ويتحول لفلوس»، «النويز كثير»، «خل الإضاءة الزرقاء تأثر على الفلوس بس». الـSkill تشتغل لحالها.
بعد ما تخلص المشروع: «سوي retro» أو «احفظ اللي تعلمناه».

## تطوير المعرفة
- القاعدة اللي اشتغلت مرة = `Candidate`. لو اشتغلت في مشروع ثاني = `Proven`.
- لا تحط معلومات خاصة (IP، مسارات جهازك، أسماء عملاء، توكنات). سكيل الـretro يفحصها قبل الحفظ.

## Changelog
- 1.0.0 — أول نسخة، من مشروع «Laptop → Money» (EEVEE، Turntable + Match cut).
