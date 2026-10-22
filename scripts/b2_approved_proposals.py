"""User-approved B2 alternatives adopted on 2026-10-22 (revision 106)."""
import math

APPROVED=frozenset(['thermal.window', 'thermal.room-split', 'construction.studs-toggle', 'pile.load-points', 'pile.cpts', 'pile.optimization', 'pile.tip-regions', 'pile.load-groups', 'quotation.type-private', 'quotation.payment-terms', 'report.view-main-contract', 'report.view-subcontract', 'report.view-tender', 'report.view-estimate', 'calc.quantities-visible', 'calc.grid-standard', 'calc.grid-wpcalc', 'calc.grid-simple', 'calc.chapter', 'workspace.dock-back', 'calc.hsb-wizard', 'symbol.category-electric', 'symbol.category-custom', 'assistant.translate', 'assistant.summarize', 'format.custom-color', 'page.replace', 'page.insert-file', 'image.embedded-edit', 'panel.attachments', 'file.place-add', 'drawing.settings', 'bcf.import', 'planning.calculate', 'report.workspace', 'wbs.auto-number', 'panel.warnings', 'table.columns', 'planning.status-date', 'layout.manage', 'company.library', 'calendar.promote-menu', 'calendar.edit', 'resource.unlink-library', 'ai.read-only-toggle', 'backup.auto', 'backup.create', 'backup.folder', 'update.install', 'documents.overview', 'documents.new-or-open', 'capture.annotate', 'status.schedule-preview', 'status.schedule-last-result', 'library.link-recognized', 'status.library-item-missing', 'status.library-item-deviated', 'status.hour-data', 'status.structure-locked', 'calendar.holiday-add', 'calendar.copy-workdays'])

def approved_construction(key,size):
    # Import after b2_geometry is initialized; keep the reviewed construction exact.
    from build_b2_analysis_drafts import proposal
    model=proposal(key,size)
    if model is None:raise ValueError('Missing approved B2 proposal: '+key)
    for part in model.paths:
        points=[]
        for point in part['points']:
            if not points or math.dist(points[-1],point)>1e-6:points.append(point)
        part['points']=points
    return model
