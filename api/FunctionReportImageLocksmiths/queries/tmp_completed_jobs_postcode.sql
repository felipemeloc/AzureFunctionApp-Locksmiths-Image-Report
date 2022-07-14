------------- Today's jobs/revenue by locksmiths (POSTCODE)
SELECT
CASE SB.RecipientName WHEN 'WGTK - Alex Skellett (A)' THEN 'Alex skellett'
						WHEN 'WGTK - Alex Skellett (V)' THEN 'Alex skellett'
						WHEN 'WGTK - Blain Harper (A)' THEN 'Blain harper'
						WHEN 'WGTK - Blain Harper (V)' THEN 'Blain harper'
						WHEN 'WGTK - Chris Webster (A)' THEN 'Chris webster'
						WHEN 'WGTK - Chris Webster (V)' THEN 'Chris webster'
						WHEN 'WGTK - Connor Todd (A)' THEN 'Connor todd'
						WHEN 'WGTK - Connor Todd (V)' THEN 'Connor todd'
						WHEN 'WGTK - Dan Fearn (A)' THEN 'Dan fearn'
						WHEN 'WGTK - Dan Fearn (V)' THEN 'Dan fearn'
						WHEN 'WGTK Dan Fearn (A) (038)' THEN 'Dan fearn'
						WHEN 'WGTK Dan Fearn (V) (038)' THEN 'Dan fearn'
						WHEN 'WGTK - Danny Instone (A)' THEN 'Danny instone'
						WHEN 'WGTK - Danny Instone (V)' THEN 'Danny instone'
						WHEN 'WGTK - Hannah Kirkhouse (A)' THEN 'Hannah kirkhouse'
						WHEN 'WGTK - JAMES TAYLOR' THEN 'James taylor'
						WHEN 'WGTK - James Taylor (A)' THEN 'James taylor'
						WHEN 'WGTK - James Taylor (V)' THEN 'James taylor'
						WHEN 'WGTK - Jamie Steer (A)' THEN 'Jamie steer'
						WHEN 'WGTK - John Middleton (A)' THEN 'John middleton'
						WHEN 'WGTK - John Middleton (V)' THEN 'John middleton'
						WHEN 'WGTK - Josh Sussex (V)' THEN 'Josh sussex'
						WHEN 'WGTK - Lee Denton (A)' THEN 'Lee denton'
						WHEN 'WGTK - Lee Denton (V)' THEN 'Lee denton'
						WHEN 'WGTK - Liam Smith (V)' THEN 'Liam smith'
						WHEN 'WGTK - Lucy Cann (V)' THEN 'Lucy cann'
						WHEN 'WGTK - Mark Neale (A)' THEN 'Mark neale'
						WHEN 'WGTK - River Dunn (A)' THEN 'River dunn'
						WHEN 'WGTK - River Dunn (V)' THEN 'River dunn'
						WHEN 'WGTK - Sean Green (V)' THEN 'Sean green'
						WHEN 'WGTK - Usman Azhar' THEN 'Usman azhar'
						WHEN 'WGTK - Usman Azhar (A)' THEN 'Usman azhar'
						WHEN 'WGTK - Usman Azhar (V)' THEN 'Usman azhar'
						WHEN 'WGTK - ALEX' THEN 'Alex skellett'
						WHEN 'WGTK - Alex (A)' THEN 'Alex skellett'
						WHEN 'WGTK - Lucy (V)' THEN 'Lucy cann'
						WHEN 'WGTK - Blain (A)' THEN 'Blain harper'
						WHEN 'WGTK - Blain (V)' THEN 'Blain harper'
						WHEN 'WGTK - Liam (V)' THEN 'Liam smith'
						WHEN 'WGTK - CHRIS ' THEN 'Chris webster'
						WHEN 'WGTK - Chris (A)' THEN 'Chris webster'
						WHEN 'WGTK - Connor' THEN 'Connor todd'
						WHEN 'WGTK - Connor (V)' THEN 'Connor todd'
						WHEN 'WGTK - Hannah' THEN 'Hannah kirkhouse'
						WHEN 'WGTK - Hannah (A)' THEN 'Hannah kirkhouse'
						WHEN 'WGTK - Jamie ' THEN 'Jamie steer'
						WHEN 'WGTK - Jamie (A)' THEN 'Jamie steer'
						WHEN 'WGTK - John ' THEN 'John middleton'
						WHEN 'WGTK - John (A)' THEN 'John middleton'
						WHEN 'WGTK - Josh (A)' THEN 'Josh sussex'
						WHEN 'WGTK - Josh (V)' THEN 'Josh sussex'
						WHEN 'WGTK - LEE' THEN 'Lee denton'
						WHEN 'WGTK - Mark' THEN 'Mark neale'
						WHEN 'WGTK - River' THEN 'River dunn'
						WHEN 'WGTK - River (a)' THEN 'River dunn'
						WHEN 'WGTK - Sean (A)' THEN 'Sean green'
						WHEN 'WGTK - Sean (V)' THEN 'Sean green'
					ELSE SB.RecipientName
END AS "Locksmith",
SB.LocksmithPostCode,
SB.ReportID
FROM 
(
SELECT
DISTINCT(LD.ReportID),
CK.LocksmithPostCode,
PF.RecipientName,
PF.NetCost
FROM [dbo].[Policy_LocksmithDetails] LD
LEFT JOIN [dbo].[Policy_Financial] PF
ON LD.ReportID = PF.ReportID
LEFT JOIN [dbo].[Policy_ClaimDetails_Key] CK
ON LD.ReportID = CK.ReportID
WHERE LD.Selected = 1
AND PF.RecipientName LIKE ('WGTK%')
AND LD.ReportID IN (
	SELECT
	DISTINCT(PD.ReportID)
	FROM
	[dbo].[Policy_Diary] PD
	WHERE PD.Active = 0
	AND CAST(PD.ClosedDate AS DATE) = '{TARGET_DATE}'
)
AND CAST(LD.AvailableFromDate AS DATE) = '{TARGET_DATE}'
) AS SB
WHERE SB.NetCost IS NOT NULL
GROUP BY SB.RecipientName, SB.LocksmithPostCode, SB.ReportID;