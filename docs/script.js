// Constants for company and domain exclusions
const EXCLUDED_COMPANIES = new Set([
    "Alanah Phillips", "Alliant Engineering", "Alpha Financial Advisors", "AlphaK", "Behavioral Economics",
    "BlueRock Wealth Management Inc", "Boys without Fathers", "Bph Wealth Management LLP", "Brave Eagle Wealth",
    "BzzTxt, LLC", "Camelotta Advisors", "Campbell Financial Services", "Canaccord Genuity", "Change Is The Future",
    "Columbia Threadneedle Investment", "Consilium Associates", "Consultant DNA", "Courageous Business Culture",
    "Danielson Group Wealth Management", "DEMA Health Ltd Co", "Denison Financial", "DigitalScan4Events",
    "DreamSmart Academy, LLC", "DreamSmart Behavioral Solutions, LLC", "Edward Jones", "Eighty20 Virtual Corp",
    "Equilibrium Financial Planning LLP", "Evans Wealth Management", "Family Wealth Alliance", "FDNA InvestorTrial",
    "Finwizdom", "Fireseeds", "Fivestone Studios", "Freedom Empire Consulting", "Gigaplex", "Gill Capital",
    "Gillian Dunn", "Global Executive Business Consultants", "GRS Creates", "Gwen Smith", "IFC Bank", "InfOpinion Gmbh",
    "InstructAnt Financial Solutions", "Intel Corp", "IVV", "Legacy Family Office - 2020", "Legacy Movement",
    "Legacy Planning Advisors LLC", "Lehare Pty Ltd", "Luminous Wealth, LLC", "M4A3", "MacDonald Financial",
    "Mark Keith Services", "Mark Murphy", "Maximum Impact Partners, Inc.", "Merit Corporate", "Merit Financial",
    "Merit Financial Advisors", "Merit Financial Demo", "Merlynn Intelligence Technologies Corporation",
    "Merrill (The Farret Group)", "My Brilliant Fit Pty Ltd", "My Future Capacity", "My Junior Advisor",
    "Napa Wealth Managment", "NBFWM Bluteau Caseley Wealth Management Group", "Next Chapter", "OceanFront Wealth Inc.",
    "Patel Capital Partners", "Post Release", "Providence Wealth", "Pro-vision Lifestyles Ltd", "Rafael Nars",
    "Raymond James Ltd.", "Rejane Tamoto", "RentScale", "Richardson Wealth", "Ridgeline Coaching",
    "Robertson Stephens Wealth Management", "Selcouth Coaching & Consulting", "Shelley Row Associates LLC",
    "Single Point Partners", "Sirenusa Consortium LLC", "Splendys Planejamento Financeiro Pessoal & Assessoria",
    "Stout", "Suncoast Advisory", "Sykon Capital LLC", "SYNERGY HomeCare", "The Covenant Group",
    "The Initiative for Family Business & Entrepreneurship", "The Millstone Evans Group of Raymond James",
    "The Wealth Consulting Group", "Timonier", "Transform Group LLC", "Triad Partners", "Triple Partners",
    "Vickery Financial Services", "WealthUp", "Wired2Perform", "Worxbee", "XPO Brands"
]);

const EXCLUDED_DOMAINS = new Set([
    "https://alliant-inc.com", "https://alphafa.com", "https://alphakholdings.com", "https://bluerockwealth.ca",
    "https://bphwealth.co.uk", "https://www.braveeaglewealth.com", "https://bzztxt.com", "https://camelotta.com",
    "https://campbell.financial", "https://campbellfs.com", "https://www.canaccordgenuity.com",
    "https://samanthachambers.com", "https://columbiathreadneedle.com", "https://www.consilium-llc.net",
    "https://www.consiliumcorporation.com", "https://danielsongroup.ca", "https://demahealth.com",
    "https://dreamsmartacademy.com", "https://dreamsmartbehavioralsolutions.com", "http://www.edwardjones.com",
    "https://www.eighty20.co.za", "https://equilibrium.co.uk", "https://evanswealthmanagement.com",
    "https://www.ewmstanevans.com", "https://www.familywealthalliance.com", "https://www.finwizdom.com",
    "https://fireseeds.com", "https://fivestonestudios.com", "https://freedomempireconsulting.com",
    "https://www.gillinvest.com", "https://www.gilliandunn.com", "https://globalexecutivebusinessconsultants.com",
    "https://grscreates.com", "https://gwensmith.net", "https://www.ifc.org", "https://infopinion.com.br",
    "https://instructant.com.au", "https://intel.com/", "https://ivv-vermogensopbouw.nl",
    "https://www.legacyplanningadvisors.com", "https://insolvencynotices.com.au/company/le-hare-pty-ltd",
    "https://www.luminouswealth.com", "https://macdonaldfinancial.com", "https://jmcwealth.com",
    "https://www.gotimpact.com", "https://www.meritfinancialadvisors.com", "https://www.merlynn-ai.com",
    "https://www.ml.com", "https://napawealth.com", "https://www.bdcwealth.ca", "https://proximocapitulo.pt",
    "https://www.oceanfrontwealth.com", "https://patelcapital.us", "https://patelcapitalgroups.com",
    "https://providencewealth.com.au", "https://www.raymondjames.com", "https://rejanetamoto.com.br",
    "https://rentscale.com", "https://richardsonwealth.com", "https://ridgelinecoaching.com", "https://rscapital.com",
    "https://www.selcouthconsultancy.com", "https://spcfo.com", "https://sirenusa-consortium-llc.square.site",
    "https://www.splendys.net", "https://suncoastadvisorygroup.com", "https://www.sykoncapital.com",
    "https://synergyhomecare.com", "https://www.covenant-group.com", "https://www.sju.edu",
    "https://www.millstoneevansgroup.com", "https://www.wealthcg.com", "https://www.timonier.com",
    "https://transformgroup.com", "https://triadpartners.com", "https://www.triplepartners.com",
    "https://www.vickeryfin.net", "https://www.wealthup.co.za", "https://worxbee.com"
]);

// Helper functions
function parseDate(dateStr) {
    if (!dateStr) return null;
    try {
        if (dateStr instanceof Date) return dateStr;
        dateStr = String(dateStr).trim();
        if (!dateStr || ['', 'nan', 'none', 'null'].includes(dateStr.toLowerCase())) return null;
        return new Date(dateStr);
    } catch {
        return null;
    }
}

function getCurrentESTTime() {
    const now = new Date();
    return {
        date: now.toLocaleDateString('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }),
        time: now.toLocaleTimeString('en-US', {
            timeZone: 'America/New_York',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
        }) + ' EST'
    };
}

function showAlert(message, type = 'danger') {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `glass-alert alert-${type} mb-4`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
        ${message}
    `;
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alertDiv);
}

function processVisitData(data, timePeriodDays) {
    try {
        // Validate required columns
        const requiredCols = ['Name', 'Last visit', 'Unique pages Visited'];
        const missingCols = requiredCols.filter(col => !data[0].hasOwnProperty(col));
        if (missingCols.length > 0) {
            throw new Error(`Missing required columns: ${missingCols.join(', ')}. Please ensure this is a Snitcher export file.`);
        }

        // Get all valid dates
        const allDates = data
            .map(row => parseDate(row['Last visit']))
            .filter(date => date !== null);

        if (allDates.length === 0) {
            throw new Error('No valid visit dates found in the file.');
        }

        // Find the latest date
        const latestDate = new Date(Math.max.apply(null, allDates));
        const reportEnd = latestDate;
        const reportStart = new Date(reportEnd);
        reportStart.setDate(reportStart.getDate() - timePeriodDays);

        // Filter and process valid visits
        const validVisits = data
            .filter(row => {
                if (!row.Name || !row['Last visit']) return false;
                
                // Exclude by company name
                if (EXCLUDED_COMPANIES.has(row.Name.trim())) return false;
                
                // Exclude by domain
                const pagesVisited = String(row['Unique pages Visited'] || '');
                if ([...EXCLUDED_DOMAINS].some(domain => pagesVisited.includes(domain))) return false;

                const lastVisit = parseDate(row['Last visit']);
                return lastVisit && lastVisit >= reportStart && lastVisit <= reportEnd;
            })
            .map(row => ({
                name: row.Name,
                lastVisit: parseDate(row['Last visit']),
                pages: row['Unique pages Visited'] || ''
            }));

        if (validVisits.length === 0) {
            const period = `${timePeriodDays} day${timePeriodDays > 1 ? 's' : ''}`;
            throw new Error(`No visits found in the last ${period} ending ${latestDate.toLocaleString()}.`);
        }

        // Sort by last visit descending and remove duplicates
        validVisits.sort((a, b) => b.lastVisit - a.lastVisit);
        const uniqueCompanies = Object.values(
            validVisits.reduce((acc, visit) => {
                if (!acc[visit.name]) acc[visit.name] = visit;
                return acc;
            }, {})
        );

        // Sort final results by time ascending
        uniqueCompanies.sort((a, b) => a.lastVisit - b.lastVisit);

        // Format visits
        const formattedVisits = uniqueCompanies.map(visit => {
            let action = 'visited homepage';
            const pagesStr = String(visit.pages);

            if (pagesStr && !['hsCtaTracking', '_hcms'].some(indicator => pagesStr.includes(indicator))) {
                const firstPage = pagesStr.split(/[,;]/)[0].trim();
                if (firstPage && firstPage !== '/') {
                    try {
                        let path;
                        if (firstPage.startsWith('http')) {
                            const url = new URL(firstPage);
                            path = url.pathname.slice(1);
                        } else {
                            path = firstPage.replace(/^\//, '');
                        }

                        if (path) {
                            let segments = path.split('/');
                            let lastSegment = segments[segments.length - 1];

                            if (!lastSegment || /^\d+$/.test(lastSegment) || lastSegment.length < 3) {
                                lastSegment = segments.length > 1 ? segments[segments.length - 2] : segments[0];
                            }

                            if (lastSegment) {
                                const formattedAction = lastSegment
                                    .replace(/\.[^.]*$/, '')
                                    .replace(/[-_]/g, ' ')
                                    .trim()
                                    .toLowerCase();
                                if (formattedAction) action = `viewed ${formattedAction}`;
                            }
                        }
                    } catch (e) {
                        console.error('Error parsing URL:', e);
                    }
                }
            }

            return `${visit.name}, ${action}`;
        });

        // Get current EST time
        const estTime = getCurrentESTTime();
        
        // Update timestamp display
        document.getElementById('generationDate').textContent = estTime.date;
        document.getElementById('generationTime').textContent = estTime.time;

        // Return formatted report
        return `Here is the daily snitcher update as of ${estTime.date}, ${estTime.time}\n\n${formattedVisits.join('\n\n')}`;
    } catch (error) {
        throw new Error(`Error processing data: ${error.message}`);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize clocks
    updateClocks();
    setInterval(updateClocks, 1000);

    // File input handling
    document.getElementById('file').addEventListener('change', function(e) {
        const labelText = document.getElementById('labelText');
        if (e.target.files.length > 0) {
            labelText.textContent = e.target.files[0].name;
        } else {
            labelText.textContent = 'Choose Snitcher export file (CSV or Excel)';
        }
    });

    // Generate button click handler
    document.getElementById('generateBtn').addEventListener('click', async function() {
        const fileInput = document.getElementById('file');
        const timePeriod = parseInt(document.getElementById('time_period').value) || 1;
        const btn = this;

        if (!fileInput.files.length) {
            showAlert('Please select a file first.');
            return;
        }

        const file = fileInput.files[0];
        if (!/\.(csv|xlsx|xls)$/i.test(file.name)) {
            showAlert('Please upload a CSV or Excel file.');
            return;
        }

        // Disable button and show loading state
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';

        try {
            const data = await new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = async function(e) {
                    try {
                        let data;
                        if (file.name.toLowerCase().endsWith('.csv')) {
                            // Parse CSV
                            const text = e.target.result;
                            const rows = text.split(/\\r?\\n/);
                            const headers = rows[0].split(',').map(h => h.trim());
                            data = rows.slice(1)
                                .filter(row => row.trim())
                                .map(row => {
                                    const values = row.split(',');
                                    return headers.reduce((obj, header, i) => {
                                        obj[header] = values[i];
                                        return obj;
                                    }, {});
                                });
                        } else {
                            // Parse Excel
                            const workbook = XLSX.read(e.target.result, { type: 'array' });
                            const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                            data = XLSX.utils.sheet_to_json(firstSheet);
                        }
                        resolve(data);
                    } catch (error) {
                        reject(error);
                    }
                };
                reader.onerror = () => reject(new Error('Error reading file'));
                
                if (file.name.toLowerCase().endsWith('.csv')) {
                    reader.readAsText(file);
                } else {
                    reader.readAsArrayBuffer(file);
                }
            });

            const report = processVisitData(data, timePeriod);
            document.getElementById('reportContent').textContent = report;
            document.getElementById('reportSection').style.display = 'block';
            document.getElementById('alertContainer').innerHTML = '';

        } catch (error) {
            showAlert(error.message);
            document.getElementById('reportSection').style.display = 'none';
        } finally {
            // Reset button state
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate Report';
        }
    });
});

// Clock update function
function updateClocks() {
    const now = new Date();
    
    // Local time
    document.getElementById('localTime').textContent = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
    document.getElementById('localDate').textContent = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    // EST time
    const estOptions = { timeZone: 'America/New_York' };
    document.getElementById('estTime').textContent = now.toLocaleTimeString('en-US', {
        ...estOptions,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
    document.getElementById('estDate').textContent = now.toLocaleDateString('en-US', {
        ...estOptions,
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Copy functionality
function copyReportText() {
    const reportElement = document.querySelector('.report-preview pre');
    if (reportElement) {
        const reportText = reportElement.textContent;
        navigator.clipboard.writeText(reportText).then(function() {
            const button = event.target.closest('.btn-copy');
            button.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy me-2"></i>Copy Report';
            }, 2000);
        });
    }
}